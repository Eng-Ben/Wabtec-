from datetime import datetime
import json

from database import init_db, save_pressure_samples, save_test_result
from input_reader import read_valve_code
from plc_client import run_plc_test
from report import generate_pdf_report


def load_json(path):
    # Loads JSON configuration files used to select the correct test program.
    with open(path, "r") as file:
        return json.load(file)


def main():
    # Creates the database tables if they do not already exist.
    init_db()

    # valve_tests contains the actual test parameters.
    # valve_map connects the operator input to the correct test program.
    valve_tests = load_json("test_programs/valve_tests.json")
    valve_map = load_json("test_programs/valve_map.json")

    # Shows the available valve/test codes and waits for operator input.
    scanned_code = read_valve_code(list(valve_map.keys()))

    if scanned_code not in valve_map:
        print(f"Unknown valve code: {scanned_code}")
        return

    program_key = valve_map[scanned_code]

    if program_key not in valve_tests:
        print(f"No test program found for: {program_key}")
        return

    test_program = valve_tests[program_key]
    valve_id = scanned_code

    print()
    print(f"Starting test for: {valve_id}")
    print(f"Selected PLC program: {program_key}")
    print()

    # Starts the PLC communication and monitors the sequence until completion.
    result = run_plc_test(test_program)

    operator_name = input("Operator name: ").strip()
    result["operator_name"] = operator_name

    # Creates a unique test ID based on the current date and time.
    test_id = datetime.now().strftime("TEST-%Y%m%d-%H%M%S")
    result["test_id"] = test_id

    # Stores the main test result and the logged sequence samples in SQLite.
    save_test_result(valve_id, result)
    save_pressure_samples(test_id, result["pressure_series"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = f"reports/{valve_id}_{timestamp}.pdf"

    # Generates a PDF report from the collected test data.
    generate_pdf_report(result, pdf_path)

    print()
    print(f"PDF report created: {pdf_path}")
    print("Inspection complete")
    print()


if __name__ == "__main__":
    main()
