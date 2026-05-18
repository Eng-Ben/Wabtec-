import asyncio
import random
import time

from asyncua import Client

from config import OPC_SERVER_URL, OPC_NODES


async def run_plc_test(test_program):

    async with Client(url=OPC_SERVER_URL) as client:

        nodes = {
            name: client.get_node(node_id)
            for name, node_id in OPC_NODES.items()
        }

        # Reset start signal before test
        await nodes["start_test"].write_value(False)
        await asyncio.sleep(0.2)

        # Start PLC sequence
        await nodes["start_test"].write_value(True)

        pressure_series = []

        start_time = time.time()

        test_type = test_program.get("test_type", "standard")

        pressure_setpoint = test_program["pressure_setpoint"]

        current_pressure = 0.0

        # -----------------------------
        # PRESSURE BUILD-UP PHASE
        # -----------------------------

        while current_pressure < pressure_setpoint:

            elapsed_time = time.time() - start_time

            current_pressure += random.uniform(0.2, 0.7)

            current_pressure = round(
                min(current_pressure, pressure_setpoint),
                2
            )

            pressure_series.append({
                "time": round(elapsed_time, 1),
                "pressure": current_pressure
            })

            await asyncio.sleep(0.5)

        # -----------------------------
        # PRESSURE HOLD TEST
        # -----------------------------

        if test_type == "pressure_hold":

            hold_start_pressure = current_pressure

            hold_time = test_program["hold_time_seconds"]

            hold_start_time = time.time()

            while (time.time() - hold_start_time) < hold_time:

                elapsed_time = time.time() - start_time

                # Simulate small pressure decay
                current_pressure -= random.uniform(0.00, 0.03)

                current_pressure = round(current_pressure, 2)

                pressure_series.append({
                    "time": round(elapsed_time, 1),
                    "pressure": current_pressure
                })

                await asyncio.sleep(0.5)

            hold_end_pressure = current_pressure

            pressure_drop = round(
                hold_start_pressure - hold_end_pressure,
                2
            )

            passed = (
                pressure_drop
                <= test_program["max_pressure_drop"]
            )

        # -----------------------------
        # STANDARD TEST
        # -----------------------------

        else:

            pressure_drop = 0.0

            hold_start_pressure = current_pressure
            hold_end_pressure = current_pressure

            passed = (
                test_program["min_pressure"]
                <= current_pressure
                <= test_program["max_pressure"]
            )

        # Wait for PLC completion signal
        while True:

            test_done = await nodes["test_done"].read_value()

            if test_done:
                break

            await asyncio.sleep(0.2)

        # Reset start signal
        await nodes["start_test"].write_value(False)

        return {

            "program_id": test_program["program_id"],

            "valve_type": test_program["valve_type"],

            "test_type": test_type,

            "pressure_setpoint": pressure_setpoint,

            "measured_pressure": current_pressure,

            "min_pressure": test_program["min_pressure"],

            "max_pressure": test_program["max_pressure"],

            "hold_time_seconds": test_program.get(
                "hold_time_seconds",
                0
            ),

            "start_hold_pressure": hold_start_pressure,

            "end_hold_pressure": hold_end_pressure,

            "pressure_drop": pressure_drop,

            "max_pressure_drop": test_program.get(
                "max_pressure_drop",
                0
            ),

            "test_duration_seconds": round(
                time.time() - start_time,
                1
            ),

            "alarm_status": 0,

            "result": "PASS" if passed else "FAIL",

            "pressure_series": pressure_series
        }