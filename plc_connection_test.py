import asyncio
from asyncua import Client
from config import OPC_SERVER_URL, OPC_NODES


async def test_plc_connection():

    print("\n==============================")
    print("PLC CONNECTION TEST STARTED")
    print("==============================\n")

    print(f"[INFO] OPC Server URL: {OPC_SERVER_URL}")

    try:

        async with Client(url=OPC_SERVER_URL) as client:

            print("[PASS] Connected to OPC server\n")

            # -----------------------------
            # LOAD NODES
            # -----------------------------

            try:
                start_test_node = client.get_node(
                    OPC_NODES["start_test"]
                )

                print("[PASS] Found start_test node")

            except Exception as e:
                print(f"[FAIL] Could not load start_test node: {e}")
                return

            try:
                test_done_node = client.get_node(
                    OPC_NODES["test_done"]
                )

                print("[PASS] Found test_done node")

            except Exception as e:
                print(f"[FAIL] Could not load test_done node: {e}")
                return

            print()

            # -----------------------------
            # READ TEST
            # -----------------------------

            try:

                test_done = await test_done_node.read_value()

                print(
                    f"[PASS] Read TestDone value: {test_done}"
                )

            except Exception as e:

                print(
                    f"[FAIL] Could not read TestDone: {e}"
                )

            # -----------------------------
            # WRITE TEST
            # -----------------------------

            try:

                await start_test_node.write_value(False)

                print(
                    "[PASS] Successfully wrote StartTest=False"
                )

            except Exception as e:

                print(
                    f"[FAIL] Could not write StartTest: {e}"
                )

            print("\n==============================")
            print("PLC CONNECTION TEST COMPLETE")
            print("==============================\n")

    except Exception as e:

        print("\n[FAIL] Could not connect to OPC server")
        print(f"[ERROR] {e}\n")


if __name__ == "__main__":
    asyncio.run(test_plc_connection())