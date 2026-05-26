from report import generate_pdf_report
from datetime import datetime

import json

from input_reader import read_valve_code
from plc_client import run_plc_test
from database import init_db, save_test_result, save_pressure_samples


def load_json(path):
    with open(path, "r") as file:
        return json.load(file)


def main():
    init_db()

    valve_tests = load_json("test_programs/valve_tests.json")
    valve_map = load_json("test_programs/valve_map.json")

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

    result = run_plc_test(test_program)

    operator_name = input("Operator name: ").strip()

    result["operator_name"] = operator_name

    test_id = datetime.now().strftime("TEST-%Y%m%d-%H%M%S")
    result["test_id"] = test_id

    save_test_result(valve_id, result)
    save_pressure_samples(test_id, result["pressure_series"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = f"reports/{valve_id}_{timestamp}.pdf"

    generate_pdf_report(result, pdf_path)

    print()
    print(f"PDF report created: {pdf_path}")
    print("Inspection complete")
    print()


if __name__ == "__main__":
    main()
