import asyncio
import random

from asyncua import Server


async def reset_states(
    start_test,
    test_done,
    test_passed,
    alarm_status,
    measured_pressure,
    step_1,
    step_2,
    step_3,
    step_4,
    step_5,
    step_6,
    v5,
    v6,
    v9,
):
    await start_test.write_value(False)
    await test_done.write_value(False)
    await test_passed.write_value(False)
    await alarm_status.write_value(0)
    await measured_pressure.write_value(0.0)

    await step_1.write_value(False)
    await step_2.write_value(False)
    await step_3.write_value(False)
    await step_4.write_value(False)
    await step_5.write_value(False)
    await step_6.write_value(False)

    await v5.write_value(False)
    await v6.write_value(False)
    await v9.write_value(False)


async def main():
    server = Server()

    await server.init()

    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    uri = "WabtecPressureTestSystem"
    idx = await server.register_namespace(uri)

    objects = server.nodes.objects

    test_control = await objects.add_object(
        f"ns={idx};s=DB_TestControl", "DB_TestControl"
    )

    start_test = await test_control.add_variable(
        f"ns={idx};s=StartTest", "StartTest", False
    )

    selected_program_id = await test_control.add_variable(
        f"ns={idx};s=SelectedProgramID", "SelectedProgramID", 0
    )

    pressure_setpoint = await test_control.add_variable(
        f"ns={idx};s=PressureSetpoint", "PressureSetpoint", 0.0
    )

    min_pressure = await test_control.add_variable(
        f"ns={idx};s=MinPressure", "MinPressure", 0.0
    )

    max_pressure = await test_control.add_variable(
        f"ns={idx};s=MaxPressure", "MaxPressure", 0.0
    )

    test_duration = await test_control.add_variable(
        f"ns={idx};s=TestDuration", "TestDuration", 0
    )

    test_done = await test_control.add_variable(
        f"ns={idx};s=TestDone", "TestDone", False
    )

    measured_pressure = await test_control.add_variable(
        f"ns={idx};s=MeasuredPressure", "MeasuredPressure", 0.0
    )

    test_passed = await test_control.add_variable(
        f"ns={idx};s=TestPassed", "TestPassed", False
    )

    alarm_status = await test_control.add_variable(
        f"ns={idx};s=AlarmStatus", "AlarmStatus", 0
    )

    step_1 = await test_control.add_variable(f"ns={idx};s=step_1", "step_1", False)

    step_2 = await test_control.add_variable(f"ns={idx};s=step_2", "step_2", False)

    step_3 = await test_control.add_variable(f"ns={idx};s=step_3", "step_3", False)

    step_4 = await test_control.add_variable(f"ns={idx};s=step_4", "step_4", False)

    step_5 = await test_control.add_variable(f"ns={idx};s=step_5", "step_5", False)

    step_6 = await test_control.add_variable(f"ns={idx};s=step_6", "step_6", False)

    v5 = await test_control.add_variable(f"ns={idx};s=v5", "v5", False)

    v6 = await test_control.add_variable(f"ns={idx};s=v6", "v6", False)

    v9 = await test_control.add_variable(f"ns={idx};s=v9", "v9", False)

    writable_nodes = [
        start_test,
        selected_program_id,
        pressure_setpoint,
        min_pressure,
        max_pressure,
        test_duration,
        test_done,
        measured_pressure,
        test_passed,
        alarm_status,
        step_1,
        step_2,
        step_3,
        step_4,
        step_5,
        step_6,
        v5,
        v6,
        v9,
    ]

    for node in writable_nodes:
        await node.set_writable()

    print("OPC UA Simulation Server Started")
    print(f"Namespace index: {idx}")

    async with server:
        test_running = False

        while True:
            start = await start_test.read_value()

            if start and not test_running:
                test_running = True

                print("SIMULATED TEST STARTED")

                await reset_states(
                    start_test,
                    test_done,
                    test_passed,
                    alarm_status,
                    measured_pressure,
                    step_1,
                    step_2,
                    step_3,
                    step_4,
                    step_5,
                    step_6,
                    v5,
                    v6,
                    v9,
                )

                await start_test.write_value(True)

                min_p = await min_pressure.read_value()
                max_p = await max_pressure.read_value()
                duration = await test_duration.read_value()

                current_pressure = 0.0
                simulated_pressure = 0.0

                if duration <= 0:
                    duration = 10

                steps = int(duration * 2)

                print("STEP 1: Filling")

                await step_1.write_value(True)
                await v5.write_value(True)

                for _ in range(max(1, steps // 3)):
                    target_pressure = random.uniform(min_p, max_p)

                    current_pressure += (target_pressure - current_pressure) * 0.35

                    simulated_pressure = round(current_pressure, 2)

                    await measured_pressure.write_value(simulated_pressure)

                    await asyncio.sleep(0.5)

                await step_1.write_value(False)

                print("STEP 2: Stabilizing")

                await step_2.write_value(True)

                for _ in range(max(1, steps // 3)):
                    target_pressure = random.uniform(min_p, max_p)

                    current_pressure += (target_pressure - current_pressure) * 0.20

                    simulated_pressure = round(current_pressure, 2)

                    await measured_pressure.write_value(simulated_pressure)

                    await asyncio.sleep(0.5)

                await step_2.write_value(False)

                print("STEP 3: Holding")

                await step_3.write_value(True)

                for _ in range(max(1, steps // 3)):
                    current_pressure -= random.uniform(0.00, 0.03)

                    simulated_pressure = round(current_pressure, 2)

                    await measured_pressure.write_value(simulated_pressure)

                    await asyncio.sleep(0.5)

                await step_3.write_value(False)
                await v5.write_value(False)

                print("STEP 4: Venting")

                await step_4.write_value(True)
                await v6.write_value(True)

                await asyncio.sleep(1)

                await step_4.write_value(False)
                await v6.write_value(False)

                print("STEP 5: Finishing")

                await step_5.write_value(True)

                await asyncio.sleep(1)

                await step_5.write_value(False)

                print("STEP 6: Complete")

                await step_6.write_value(True)
                await v9.write_value(True)

                passed = min_p <= simulated_pressure <= max_p

                await test_passed.write_value(passed)
                await alarm_status.write_value(0)

                await asyncio.sleep(1)

                await test_done.write_value(True)

                print("SIMULATED TEST COMPLETE")

                await asyncio.sleep(1)

                await step_6.write_value(False)
                await v9.write_value(False)
                await start_test.write_value(False)

                test_running = False

            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
