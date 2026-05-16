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

        await nodes["start_test"].write_value(False)

        await nodes["selected_program_id"].write_value(test_program["program_id"])
        await nodes["pressure_setpoint"].write_value(test_program["pressure_setpoint"])
        await nodes["min_pressure"].write_value(test_program["min_pressure"])
        await nodes["max_pressure"].write_value(test_program["max_pressure"])
        await nodes["test_duration"].write_value(test_program["test_duration_seconds"])

        await nodes["start_test"].write_value(True)

        pressure_series = []
        start_time = time.time()

        while True:
            measured_pressure = await nodes["measured_pressure"].read_value()

            elapsed_time = time.time() - start_time

            pressure_series.append({
                "time": elapsed_time,
                "pressure": measured_pressure
            })

            test_done = await nodes["test_done"].read_value()

            if test_done:
                break

            await asyncio.sleep(0.5)

        measured_pressure = await nodes["measured_pressure"].read_value()
        test_passed = await nodes["test_passed"].read_value()
        alarm_status = await nodes["alarm_status"].read_value()

        await nodes["start_test"].write_value(False)

        return {
            "program_id": test_program["program_id"],
            "valve_type": test_program["valve_type"],
            "pressure_setpoint": test_program["pressure_setpoint"],
            "measured_pressure": measured_pressure,
            "min_pressure": test_program["min_pressure"],
            "max_pressure": test_program["max_pressure"],
            "test_duration_seconds": test_program["test_duration_seconds"],
            "alarm_status": int(alarm_status),
            "result": "PASS" if test_passed else "FAIL",
            "pressure_series": pressure_series
        }