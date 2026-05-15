import asyncio
import random

from asyncua import Server


async def main():

    server = Server()

    await server.init()

    # OPC UA server address
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    # Register custom namespace
    uri = "WabtecPressureTestSystem"
    idx = await server.register_namespace(uri)

    # Create object
    objects = server.nodes.objects
    test_control = await objects.add_object(idx, "DB_TestControl")

    # Create variables
    start_test = await test_control.add_variable(idx, "StartTest", False)
    selected_program_id = await test_control.add_variable(idx, "SelectedProgramID", 0)

    pressure_setpoint = await test_control.add_variable(idx, "PressureSetpoint", 0.0)
    min_pressure = await test_control.add_variable(idx, "MinPressure", 0.0)
    max_pressure = await test_control.add_variable(idx, "MaxPressure", 0.0)

    test_duration = await test_control.add_variable(idx, "TestDuration", 0)

    test_done = await test_control.add_variable(idx, "TestDone", False)

    measured_pressure = await test_control.add_variable(idx, "MeasuredPressure", 0.0)

    test_passed = await test_control.add_variable(idx, "TestPassed", False)

    alarm_status = await test_control.add_variable(idx, "AlarmStatus", 0)

    # Allow writing from client
    await start_test.set_writable()
    await selected_program_id.set_writable()

    await pressure_setpoint.set_writable()
    await min_pressure.set_writable()
    await max_pressure.set_writable()

    await test_duration.set_writable()

    print("OPC UA Server started")

    async with server:

        test_running = False

        while True:

            start = await start_test.read_value()

            if start and not test_running:

                test_running = True

                print("PLC TEST STARTED")

                await test_done.write_value(False)
                await alarm_status.write_value(0)

                setpoint = await pressure_setpoint.read_value()
                min_p = await min_pressure.read_value()
                max_p = await max_pressure.read_value()
                duration = await test_duration.read_value()

                current_pressure = 0.0
                simulated_pressure = 0.0

                steps = int(duration * 2)

                for step in range(steps):

                    target_pressure = random.uniform(min_p, max_p)

                    current_pressure += (target_pressure - current_pressure) * 0.35

                    simulated_pressure = round(current_pressure, 2)

                    await measured_pressure.write_value(simulated_pressure)

                    await asyncio.sleep(0.5)

                passed = min_p <= simulated_pressure <= max_p

                await test_passed.write_value(passed)
                await alarm_status.write_value(0)
                await test_done.write_value(True)

                print("TEST COMPLETE")

                await start_test.write_value(False)

                test_running = False

            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())