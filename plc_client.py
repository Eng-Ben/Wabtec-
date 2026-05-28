import time

import snap7
from snap7.util import get_bool, set_bool

# Static network settings for the Siemens S7-1200 PLC.
# The IP address must match the address configured in TIA Portal.
PLC_IP = "192.168.0.100"
PLC_RACK = 0
PLC_SLOT = 1


def read_m_bit(plc, byte_index, bit_index):
    # Reads one memory bit from the PLC marker area, for example M0.1.
    data = plc.mb_read(byte_index, 1)
    return get_bool(data, 0, bit_index)


def write_m_bit(plc, byte_index, bit_index, value):
    # Writes one memory bit to the PLC marker area.
    # The full byte is read first so the other bits in the same byte are not overwritten.
    data = plc.mb_read(byte_index, 1)
    set_bool(data, 0, bit_index, value)
    plc.mb_write(byte_index, 1, data)


def read_q_bit(plc, byte_index, bit_index):
    # Reads one output bit from the PLC output area, for example Q0.0.
    data = plc.ab_read(byte_index, 1)
    return get_bool(data, 0, bit_index)


def get_active_phase(step_1, step_2, step_3, step_4, step_5, step_6):
    # Converts the active PLC step bits into a readable phase name for logging and reports.
    if step_1:
        return "STEP_1"
    if step_2:
        return "STEP_2"
    if step_3:
        return "STEP_3"
    if step_4:
        return "STEP_4"
    if step_5:
        return "STEP_5"
    if step_6:
        return "STEP_6"

    return "WAITING"


def reset_sequence_steps(plc):
    # Clears the internal step bits before arming the test sequence.
    # This prevents the PLC from continuing from an old unfinished state.
    write_m_bit(plc, 0, 1, False)
    write_m_bit(plc, 0, 2, False)
    write_m_bit(plc, 0, 3, False)
    write_m_bit(plc, 0, 4, False)
    write_m_bit(plc, 0, 5, False)
    write_m_bit(plc, 0, 6, False)


def prepare_sequence_from_python(plc):
    # The Raspberry Pi does not directly start the PLC sequence.
    # It only prepares the system by setting M10.0, which is used as an enable/arm signal.
    # The actual start is still done with the physical button connected to I0.0.
    reset_sequence_steps(plc)
    time.sleep(0.2)

    write_m_bit(plc, 10, 0, True)
    print("System armed from Python: M10.0 Tag_1 = TRUE")


def run_plc_test(test_program):
    plc = snap7.client.Client()
    start_time = time.time()
    pressure_series = []

    try:
        try:
            # Opens the Snap7 connection from the Raspberry Pi to the Siemens PLC.
            plc.connect(PLC_IP, PLC_RACK, PLC_SLOT)
        except Exception as e:
            raise RuntimeError(
                f"Could not connect to PLC at {PLC_IP}. "
                "Check that the PLC is powered on, connected to the same network, "
                "and reachable from the Raspberry Pi."
            ) from e

        if not plc.get_connected():
            raise RuntimeError(
                f"Could not connect to PLC at {PLC_IP}. Snap7 connection failed."
            )

        max_test_time = test_program.get("max_test_time_seconds", 120)

        print("PLC sequence test started")
        print(f"Program: {test_program.get('valve_type')}")
        print(f"PLC IP: {PLC_IP}")
        print()

        prepare_sequence_from_python(plc)
        print("Waiting for physical button_start I0.0...")

        last_phase = "WAITING"

        while True:
            elapsed_time = time.time() - start_time

            # Reads the step bits from the PLC.
            # These marker bits represent where the Ladder sequence currently is.
            step_1 = read_m_bit(plc, 0, 1)
            step_2 = read_m_bit(plc, 0, 2)
            step_3 = read_m_bit(plc, 0, 3)
            step_4 = read_m_bit(plc, 0, 4)
            step_5 = read_m_bit(plc, 0, 5)
            step_6 = read_m_bit(plc, 0, 6)

            # Reads the relevant physical output states from the PLC.
            # These values are used for monitoring and documentation of the test run.
            light_dp = read_q_bit(plc, 0, 0)
            finish_light = read_q_bit(plc, 0, 4)
            v5 = read_q_bit(plc, 0, 5)
            v6 = read_q_bit(plc, 0, 6)
            v9 = read_q_bit(plc, 0, 7)

            active_phase = get_active_phase(
                step_1,
                step_2,
                step_3,
                step_4,
                step_5,
                step_6,
            )

            if active_phase != "WAITING":
                last_phase = active_phase

            # Stores a time sample for the report.
            # Pressure is currently set to 0 because the prototype does not read a real pressure sensor yet.
            pressure_series.append(
                {
                    "time": round(elapsed_time, 1),
                    "pressure": 0,
                    "phase": active_phase,
                }
            )

            print(
                f"Time: {round(elapsed_time, 1)}s | "
                f"Phase: {active_phase} | "
                f"S1={step_1} S2={step_2} S3={step_3} "
                f"S4={step_4} S5={step_5} S6={step_6} | "
                f"light_DP={light_dp} v5={v5} v6={v6} v9={v9} | "
                f"Done={finish_light}"
            )

            if finish_light:
                print("PLC sequence completed")

                # Disarms the PLC after the sequence is complete.
                write_m_bit(plc, 10, 0, False)
                print("System disarmed: M10.0 Tag_1 = FALSE")
                break

            if elapsed_time >= max_test_time:
                raise TimeoutError("PLC sequence timed out before finish_ligth(test).")

            time.sleep(0.5)

        return {
            "program_id": test_program.get("program_id"),
            "valve_type": test_program.get("valve_type"),
            "test_type": test_program.get("test_type"),
            "pressure_setpoint": test_program.get("pressure_setpoint", 0),
            "measured_pressure": 0,
            "min_pressure": test_program.get("min_pressure", 0),
            "max_pressure": test_program.get("max_pressure", 0),
            "hold_time_seconds": 0,
            "start_hold_pressure": 0,
            "end_hold_pressure": 0,
            "pressure_drop": 0,
            "max_pressure_drop": 0,
            "test_duration_seconds": round(time.time() - start_time, 1),
            "alarm_status": 0,
            "result": "PASS",
            "pressure_series": pressure_series,
            "last_phase": last_phase,
        }

    finally:
        try:
            plc.disconnect()
        except Exception:
            pass
