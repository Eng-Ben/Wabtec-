from datetime import datetime

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pressure_graph(test_result, graph_path):
    # Creates a simple graph from the logged pressure samples.
    # In the current prototype, pressure is set to 0 when no real pressure sensor is connected.
    # The graph structure is still kept so real pressure data can be added later.
    series = test_result["pressure_series"]

    times = [point["time"] for point in series]
    pressures = [point["pressure"] for point in series]

    plt.figure()
    plt.plot(times, pressures)
    plt.axhline(test_result["pressure_setpoint"], linestyle="--", label="Setpoint")
    plt.axhline(test_result["min_pressure"], linestyle=":", label="Min limit")
    plt.axhline(test_result["max_pressure"], linestyle=":", label="Max limit")

    plt.xlabel("Time (seconds)")
    plt.ylabel("Pressure")
    plt.title("Pressure During Test")
    plt.legend()
    plt.grid(True)

    plt.savefig(graph_path)
    plt.close()


def get_phase_summary(test_result):
    # Extracts the different PLC phases detected during the test.
    # Duplicate phases are removed so the report only shows the sequence once.
    phases = []

    for point in test_result["pressure_series"]:
        phase = point.get("phase", "UNKNOWN")

        if phase not in phases:
            phases.append(phase)

    if len(phases) > 1 and "FALLBACK_SIMULATION" in phases:
        phases.remove("FALLBACK_SIMULATION")

    return phases


def draw_fields(c, fields, x, y):
    # Helper function for writing label-value pairs in the PDF.
    c.setFont("Helvetica", 11)

    for label, value in fields:
        c.drawString(x, y, f"{label}: {value}")
        y -= 18

    return y


def generate_pdf_report(test_result, output_path):
    # Generates a PDF report from the completed PLC test result.
    graph_path = output_path.replace(".pdf", "_graph.png")
    create_pressure_graph(test_result, graph_path)

    c = canvas.Canvas(output_path, pagesize=A4)

    c.drawImage(
        "assets/wabtec_logo.png",
        400,
        760,
        width=120,
        height=50,
        preserveAspectRatio=True,
    )

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "Valve Pressure Inspection Report")

    # Shows PASS in green and FAIL in red to make the result easy to identify.
    if test_result["result"] == "PASS":
        c.setFillColor(colors.green)
    else:
        c.setFillColor(colors.red)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 760, f"Result: {test_result['result']}")
    c.setFillColor(colors.black)

    y = 720

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "GENERAL INFORMATION")
    y -= 30

    general_fields = [
        ("Test ID", test_result["test_id"]),
        ("Operator", test_result["operator_name"]),
        ("Valve Type", test_result["valve_type"]),
        ("Program ID", test_result["program_id"]),
        ("Report Generated", datetime.now().isoformat()),
    ]

    y = draw_fields(c, general_fields, 50, y)
    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "TEST PARAMETERS")
    y -= 30

    parameter_fields = [
        ("Pressure Setpoint", test_result["pressure_setpoint"]),
        ("Minimum Pressure", test_result["min_pressure"]),
        ("Maximum Pressure", test_result["max_pressure"]),
        ("Test Duration", test_result["test_duration_seconds"]),
    ]

    y = draw_fields(c, parameter_fields, 50, y)
    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "TEST RESULT")
    y -= 30

    result_fields = [
        ("Test Type", test_result["test_type"]),
        ("Measured Pressure", test_result["measured_pressure"]),
        ("Alarm Status", test_result["alarm_status"]),
        ("Final Result", test_result["result"]),
    ]

    y = draw_fields(c, result_fields, 50, y)

    # Adds extra information only for pressure hold tests.
    if test_result["test_type"] == "pressure_hold":
        y -= 20

        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "PRESSURE HOLD TEST")
        y -= 30

        hold_fields = [
            ("Hold Time (s)", test_result["hold_time_seconds"]),
            ("Start Hold Pressure", test_result["start_hold_pressure"]),
            ("End Hold Pressure", test_result["end_hold_pressure"]),
            ("Pressure Drop", test_result["pressure_drop"]),
            ("Max Allowed Drop", test_result["max_pressure_drop"]),
        ]

        y = draw_fields(c, hold_fields, 50, y)

    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "PLC PHASES DETECTED")
    y -= 20

    phases = get_phase_summary(test_result)
    phase_text = ", ".join(phases)

    c.setFont("Helvetica", 10)

    max_chars_per_line = 85
    while len(phase_text) > max_chars_per_line:
        split_index = phase_text.rfind(",", 0, max_chars_per_line)

        if split_index == -1:
            split_index = max_chars_per_line

        c.drawString(50, y, phase_text[:split_index].strip())
        phase_text = phase_text[split_index + 1 :].strip()
        y -= 14

    c.drawString(50, y, phase_text)

    c.drawImage(graph_path, 50, 60, width=500, height=230)

    c.save()
