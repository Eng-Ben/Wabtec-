from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import matplotlib.pyplot as plt


def create_pressure_graph(test_result, graph_path):
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


def generate_pdf_report(test_result, output_path):
    graph_path = output_path.replace(".pdf", "_graph.png")
    create_pressure_graph(test_result, graph_path)

    c = canvas.Canvas(output_path, pagesize=A4)

    c.drawImage(
        "assets/wabtec_logo.png",
        400,
        760,
        width=120,
        height=50,
        preserveAspectRatio=True
    )

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "Valve Pressure Inspection Report")

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

    c.setFont("Helvetica", 11)
    general_fields = [
        ("Test ID", test_result["test_id"]),
        ("Operator", test_result["operator_name"]),
        ("Valve Type", test_result["valve_type"]),
        ("Program ID", test_result["program_id"]),
        ("Report Generated", datetime.now().isoformat())
    ]

    for label, value in general_fields:
        c.drawString(50, y, f"{label}: {value}")
        y -= 18

    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "TEST PARAMETERS")
    y -= 30

    c.setFont("Helvetica", 11)
    parameter_fields = [
        ("Pressure Setpoint", test_result["pressure_setpoint"]),
        ("Minimum Pressure", test_result["min_pressure"]),
        ("Maximum Pressure", test_result["max_pressure"]),
        ("Test Duration", test_result["test_duration_seconds"])
    ]

    for label, value in parameter_fields:
        c.drawString(50, y, f"{label}: {value}")
        y -= 18

    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "TEST RESULT")
    y -= 30

    c.setFont("Helvetica", 11)
    result_fields = [

        ("Test Type", test_result["test_type"]),

        ("Measured Pressure", test_result["measured_pressure"]),

        ("Alarm Status", test_result["alarm_status"]),

        ("Final Result", test_result["result"])
    ]

    for label, value in result_fields:
        c.drawString(50, y, f"{label}: {value}")
        y -= 18
   
        # --------------------------------
        # PRESSURE HOLD TEST INFORMATION
        # --------------------------------

    if test_result["test_type"] == "pressure_hold":

        y -= 20

        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "PRESSURE HOLD TEST")

        y -= 30

        c.setFont("Helvetica", 11)

        hold_fields = [

            ("Hold Time (s)", test_result["hold_time_seconds"]),

            ("Start Hold Pressure",
            test_result["start_hold_pressure"]),

            ("End Hold Pressure",
            test_result["end_hold_pressure"]),

            ("Pressure Drop",
            test_result["pressure_drop"]),

            ("Max Allowed Drop",
            test_result["max_pressure_drop"])
        ]

        for label, value in hold_fields:

            c.drawString(50, y, f"{label}: {value}")

            y -= 18

    c.drawImage(graph_path, 50, 80, width=500, height=250)

    c.save()