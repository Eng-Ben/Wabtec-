# import asyncio
# import random
# import time
# from asyncua import Client, ua
# from config import OPC_SERVER_URL, OPC_NODES

import time
import random
import snap7
from snap7.util import get_bool, set_bool


PLC_IP = "192.168.0.100"
PLC_RACK = 0
PLC_SLOT = 1


def read_m_bit(plc, byte_index, bit_index):
    data = plc.mb_read(byte_index, 1)
    return get_bool(data, 0, bit_index)


def write_m_bit(plc, byte_index, bit_index, value):
    data = plc.mb_read(byte_index, 1)
    set_bool(data, 0, bit_index, value)
    plc.mb_write(byte_index, 1, data)


def read_q_bit(plc, byte_index, bit_index):
    data = plc.ab_read(byte_index, 1)
    return get_bool(data, 0, bit_index)


def get_active_phase(step_1, step_2, step_3, step_4, step_5, step_6):
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


def run_plc_test(test_program):
    plc = snap7.client.Client()

    try:
        plc.connect(PLC_IP, PLC_RACK, PLC_SLOT)

        if not plc.get_connected():
            raise RuntimeError("Could not connect to PLC with Snap7")

        write_m_bit(plc, 10, 0, False)
        time.sleep(0.2)

        write_m_bit(plc, 10, 0, True)

        pressure_series = []
        start_time = time.time()

        test_type = test_program.get("test_type", "standard")
        pressure_setpoint = test_program.get("pressure_setpoint", 0)
        min_pressure = test_program.get("min_pressure", 0)
        max_pressure = test_program.get("max_pressure", 10)

        current_pressure = 0.0
        hold_start_pressure = 0.0
        hold_end_pressure = 0.0
        pressure_drop = 0.0
        passed = False

        hold_started = False
        hold_start_time = None

        max_test_time = test_program.get("max_test_time_seconds", 60)
        hold_time = test_program.get("hold_time_seconds", 0)

        last_real_phase = "WAITING"

        print("PLC test started with Snap7")
        print(f"PLC IP: {PLC_IP}")
        print(f"Test type: {test_type}")
        print(f"Setpoint: {pressure_setpoint}")
        print()

        while True:
            elapsed_time = time.time() - start_time

            step_1 = read_m_bit(plc, 0, 1)
            step_2 = read_m_bit(plc, 0, 2)
            step_3 = read_m_bit(plc, 0, 3)
            step_4 = read_m_bit(plc, 0, 4)
            step_5 = read_m_bit(plc, 0, 5)
            step_6 = read_m_bit(plc, 0, 6)

            finish_light = read_q_bit(plc, 0, 4)

            v5 = read_q_bit(plc, 0, 5)
            v6 = read_q_bit(plc, 0, 6)
            v9 = read_q_bit(plc, 0, 7)
            light_dp = read_q_bit(plc, 0, 0)

            active_phase = get_active_phase(
                step_1,
                step_2,
                step_3,
                step_4,
                step_5,
                step_6
            )

            if active_phase != "WAITING":
                last_real_phase = active_phase

            if finish_light and active_phase == "WAITING":
                active_phase = last_real_phase

            if step_1:
                current_pressure += random.uniform(0.25, 0.55)

            elif step_2:
                if current_pressure < pressure_setpoint:
                    current_pressure += random.uniform(0.05, 0.20)
                else:
                    current_pressure += random.uniform(-0.03, 0.03)

            elif step_3:
                if not hold_started:
                    hold_started = True
                    hold_start_time = time.time()
                    hold_start_pressure = current_pressure

                current_pressure -= random.uniform(0.00, 0.03)

            elif step_4:
                current_pressure -= random.uniform(0.10, 0.30)

            elif step_5 or step_6:
                current_pressure += random.uniform(-0.02, 0.02)

            else:
                if current_pressure < pressure_setpoint:
                    current_pressure += random.uniform(0.25, 0.55)

                elif test_type == "pressure_hold":
                    if not hold_started:
                        hold_started = True
                        hold_start_time = time.time()
                        hold_start_pressure = current_pressure

                    current_pressure -= random.uniform(0.00, 0.03)

                else:
                    current_pressure += random.uniform(-0.02, 0.02)

            current_pressure = max(0.0, current_pressure)
            current_pressure = min(current_pressure, max_pressure + 0.5)
            current_pressure = round(current_pressure, 2)

            pressure_series.append({
                "time": round(elapsed_time, 1),
                "pressure": current_pressure,
                "phase": active_phase
            })

            print(
                f"Time: {round(elapsed_time, 1)}s | "
                f"Phase: {active_phase} | "
                f"Pressure: {current_pressure} | "
                f"S1={step_1} S2={step_2} S3={step_3} "
                f"S4={step_4} S5={step_5} S6={step_6} | "
                f"light_DP={light_dp} v5={v5} v6={v6} v9={v9} | "
                f"Done={finish_light}"
            )

            if finish_light:
                if pressure_series:
                    pressure_series[-1]["phase"] = last_real_phase

                print("PLC reported finish_ligth(test)")
                break

            if test_type == "pressure_hold" and hold_started:
                if time.time() - hold_start_time >= hold_time:
                    print("Fallback hold-time completed")
                    break

            if elapsed_time >= max_test_time:
                write_m_bit(plc, 10, 0, False)
                raise TimeoutError(
                    "PLC test timed out. finish_ligth(test) was not received."
                )

            time.sleep(0.5)

        write_m_bit(plc, 10, 0, False)

        measured_pressure = current_pressure

        if test_type == "pressure_hold":
            if hold_start_pressure == 0.0 and pressure_series:
                hold_start_pressure = max(
                    point["pressure"] for point in pressure_series
                )

            hold_end_pressure = measured_pressure

            pressure_drop = round(
                hold_start_pressure - hold_end_pressure,
                2
            )

            passed = (
                pressure_drop <= test_program.get("max_pressure_drop", 0)
                and hold_end_pressure >= min_pressure
            )

        else:
            hold_start_pressure = measured_pressure
            hold_end_pressure = measured_pressure
            pressure_drop = 0.0

            passed = min_pressure <= measured_pressure <= max_pressure

        return {
            "program_id": test_program.get("program_id"),
            "valve_type": test_program.get("valve_type"),
            "test_type": test_type,
            "pressure_setpoint": pressure_setpoint,
            "measured_pressure": measured_pressure,
            "min_pressure": min_pressure,
            "max_pressure": max_pressure,
            "hold_time_seconds": hold_time,
            "start_hold_pressure": hold_start_pressure,
            "end_hold_pressure": hold_end_pressure,
            "pressure_drop": pressure_drop,
            "max_pressure_drop": test_program.get("max_pressure_drop", 0),
            "test_duration_seconds": round(time.time() - start_time, 1),
            "alarm_status": 0,
            "result": "PASS" if passed else "FAIL",
            "pressure_series": pressure_series
        }

    finally:
        try:
            write_m_bit(plc, 10, 0, False)
        except Exception:
            pass

        try:
            plc.disconnect()
        except Exception:
            pass