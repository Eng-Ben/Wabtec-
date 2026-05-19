import asyncio
import random
import time

from asyncua import Client

from config import OPC_SERVER_URL, OPC_NODES


async def read_bool_node(nodes, node_name, default=False):
    """
    Safely read a boolean OPC node.
    If the node does not exist in the current config, return default.
    """
    if node_name not in nodes:
        return default

    try:
        return await nodes[node_name].read_value()
    except Exception:
        return default


def get_active_phase(step_1, step_2, step_3, step_4, step_5, step_6):
    """
    Convert PLC step bits into a readable phase name.
    """
    if step_1:
        return "FILLING"
    if step_2:
        return "STABILIZING"
    if step_3:
        return "HOLDING"
    if step_4:
        return "VENTING"
    if step_5:
        return "FINISHING"
    if step_6:
        return "COMPLETE"

    return "FALLBACK_SIMULATION"


async def write_if_exists(nodes, node_name, value):
    """
    Write to an OPC node only if it exists in the current config.
    """
    if node_name in nodes:
        await nodes[node_name].write_value(value)


async def run_plc_test(test_program):
    async with Client(url=OPC_SERVER_URL) as client:
        nodes = {
            name: client.get_node(node_id)
            for name, node_id in OPC_NODES.items()
        }

        await nodes["start_test"].write_value(False)
        await asyncio.sleep(0.2)

        await write_if_exists(
            nodes,
            "selected_program_id",
            test_program["program_id"]
        )

        await write_if_exists(
            nodes,
            "pressure_setpoint",
            test_program["pressure_setpoint"]
        )

        await write_if_exists(
            nodes,
            "min_pressure",
            test_program["min_pressure"]
        )

        await write_if_exists(
            nodes,
            "max_pressure",
            test_program["max_pressure"]
        )

        await write_if_exists(
            nodes,
            "test_duration",
            test_program.get("test_duration_seconds", 10)
        )

        await nodes["start_test"].write_value(True)

        pressure_series = []
        start_time = time.time()

        test_type = test_program.get("test_type", "standard")
        pressure_setpoint = test_program["pressure_setpoint"]
        min_pressure = test_program["min_pressure"]
        max_pressure = test_program["max_pressure"]

        current_pressure = 0.0
        hold_start_pressure = 0.0
        hold_end_pressure = 0.0
        pressure_drop = 0.0
        passed = False

        hold_started = False
        hold_start_time = None

        max_test_time = test_program.get("max_test_time_seconds", 60)
        hold_time = test_program.get("hold_time_seconds", 0)

        last_real_phase = "FALLBACK_SIMULATION"

        print("PLC test started")
        print(f"Test type: {test_type}")
        print(f"Setpoint: {pressure_setpoint}")
        print()

        while True:
            elapsed_time = time.time() - start_time

            step_1 = await read_bool_node(nodes, "step_1")
            step_2 = await read_bool_node(nodes, "step_2")
            step_3 = await read_bool_node(nodes, "step_3")
            step_4 = await read_bool_node(nodes, "step_4")
            step_5 = await read_bool_node(nodes, "step_5")
            step_6 = await read_bool_node(nodes, "step_6")

            test_done = await nodes["test_done"].read_value()

            active_phase = get_active_phase(
                step_1,
                step_2,
                step_3,
                step_4,
                step_5,
                step_6
            )

            if active_phase != "FALLBACK_SIMULATION":
                last_real_phase = active_phase

            if test_done and active_phase == "FALLBACK_SIMULATION":
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
                f"S4={step_4} S5={step_5} S6={step_6}"
            )

            if test_done:
                await asyncio.sleep(1)

                if "measured_pressure" in nodes:
                    measured_pressure_node = await nodes[
                        "measured_pressure"
                    ].read_value()

                    if measured_pressure_node > 0:
                        current_pressure = measured_pressure_node

                if pressure_series:
                    pressure_series[-1]["pressure"] = current_pressure
                    pressure_series[-1]["phase"] = last_real_phase

                print("PLC reported TestDone")
                break

            if test_type == "pressure_hold" and hold_started:
                if time.time() - hold_start_time >= hold_time:
                    print("Fallback hold-time completed")
                    break

            if elapsed_time >= max_test_time:
                await nodes["start_test"].write_value(False)
                raise TimeoutError(
                    "PLC test timed out. TestDone was not received."
                )

            await asyncio.sleep(0.5)

        await nodes["start_test"].write_value(False)

        measured_pressure = current_pressure

        if test_type == "pressure_hold":
            if hold_start_pressure == 0.0:
                hold_start_pressure = max(
                    point["pressure"] for point in pressure_series
                )

            hold_end_pressure = measured_pressure

            pressure_drop = round(
                hold_start_pressure - hold_end_pressure,
                2
            )

            passed = (
                pressure_drop <= test_program["max_pressure_drop"]
                and hold_end_pressure >= min_pressure
            )

        else:
            hold_start_pressure = measured_pressure
            hold_end_pressure = measured_pressure
            pressure_drop = 0.0

            passed = (
                min_pressure <= measured_pressure <= max_pressure
            )

        return {
            "program_id": test_program["program_id"],
            "valve_type": test_program["valve_type"],
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