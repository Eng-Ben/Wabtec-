import random
import time


def start_test(test_program):
    # Simulates sending the selected valve test program to the Siemens PLC
    print(f"Starting PLC test program {test_program['program_id']} for {test_program['valve_type']}")

    time.sleep(test_program["test_duration_seconds"])

    measured_pressure = round(
        random.uniform(
            test_program["min_pressure"] - 0.3,
            test_program["max_pressure"] + 0.3
        ),
        2
    )

    passed = (
        test_program["min_pressure"]
        <= measured_pressure
        <= test_program["max_pressure"]
    )

    return {
        "program_id": test_program["program_id"],
        "valve_type": test_program["valve_type"],
        "pressure_setpoint": test_program["pressure_setpoint"],
        "measured_pressure": measured_pressure,
        "min_pressure": test_program["min_pressure"],
        "max_pressure": test_program["max_pressure"],
        "test_duration_seconds": test_program["test_duration_seconds"],
        "result": "PASS" if passed else "FAIL"
    }