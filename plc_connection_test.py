import asyncio
from asyncua import Client, ua
from config import OPC_SERVER_URL, OPC_NODES


async def test_plc_connection():
    print("\n==============================")
    print("PLC CONNECTION TEST STARTED")
    print("==============================\n")

    print(f"[INFO] OPC Server URL: {OPC_SERVER_URL}")

    try:
        async with Client(url=OPC_SERVER_URL) as client:
            print("[PASS] Connected to OPC server\n")

            nodes = {}

            for name, node_id in OPC_NODES.items():
                try:
                    node = client.get_node(node_id)
                    await node.read_browse_name()
                    nodes[name] = node
                    print(f"[PASS] Found node: {name} -> {node_id}")
                except Exception as e:
                    print(f"[FAIL] Could not find node {name}: {e}")

            print()

            if "test_done" in nodes:
                try:
                    value = await nodes["test_done"].read_value()
                    print(f"[PASS] Read test_done value: {value}")
                except Exception as e:
                    print(f"[FAIL] Could not read test_done: {e}")

            if "start_test" in nodes:
                try:
                    await nodes["start_test"].write_value(
                        ua.Variant(False, ua.VariantType.Boolean)
                    )
                    print("[PASS] Wrote start_test=False")

                    await asyncio.sleep(0.5)

                    await nodes["start_test"].write_value(
                        ua.Variant(True, ua.VariantType.Boolean)
                    )
                    print("[PASS] Wrote start_test=True")

                    await asyncio.sleep(0.5)

                    await nodes["start_test"].write_value(
                        ua.Variant(False, ua.VariantType.Boolean)
                    )
                    print("[PASS] Wrote start_test=False again")

                except Exception as e:
                    print(f"[FAIL] Could not write start_test: {e}")

            print("\n==============================")
            print("PLC CONNECTION TEST COMPLETE")
            print("==============================\n")

    except Exception as e:
        print("\n[FAIL] Could not connect to OPC server")
        print(f"[ERROR] {e}\n")


if __name__ == "__main__":
    asyncio.run(test_plc_connection())