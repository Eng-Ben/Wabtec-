import json
from database import init_db, save_test_result
from plc_client import start_test


def load_test_programs():
    with open("test_programs/valve_tests.json", "r") as file:
        return json.load(file)


def select_test_program(test_programs):
    print("Available valve tests:")

    for key, program in test_programs.items():
        print(f"{key}: {program['valve_type']}")

    selected_key = input("Select valve test: ").strip().upper()

    if selected_key not in test_programs:
        raise ValueError("Invalid valve test selected")

    return test_programs[selected_key]


def main():
    init_db()

    test_programs = load_test_programs()
    selected_program = select_test_program(test_programs)

    result = start_test(selected_program)
    save_test_result(result)

    print("Inspection complete")
    print(result)


if __name__ == "__main__":
    main()