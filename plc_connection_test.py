# import asyncio
# from asyncua import Client, ua
# from config import OPC_SERVER_URL, OPC_NODES

import time
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


def test_plc_connection():
    print("\n==============================")
    print("PLC SNAP7 CONNECTION TEST STARTED")
    print("==============================\n")

    plc = snap7.client.Client()

    try:
        print(f"[INFO] Connecting to PLC at {PLC_IP}")
        plc.connect(PLC_IP, PLC_RACK, PLC_SLOT)

        if not plc.get_connected():
            print("[FAIL] Snap7 did not connect to PLC")
            return

        print("[PASS] Connected to PLC with Snap7\n")

        print("[INFO] Reading current PLC states")

        step_1 = read_m_bit(plc, 0, 1)
        step_2 = read_m_bit(plc, 0, 2)
        step_3 = read_m_bit(plc, 0, 3)
        step_4 = read_m_bit(plc, 0, 4)
        step_5 = read_m_bit(plc, 0, 5)
        step_6 = read_m_bit(plc, 0, 6)

        light_dp = read_q_bit(plc, 0, 0)
        finish_light = read_q_bit(plc, 0, 4)
        v5 = read_q_bit(plc, 0, 5)
        v6 = read_q_bit(plc, 0, 6)
        v9 = read_q_bit(plc, 0, 7)

        print(f"[INFO] step_1 M0.1: {step_1}")
        print(f"[INFO] step_2 M0.2: {step_2}")
        print(f"[INFO] step_3 M0.3: {step_3}")
        print(f"[INFO] step_4 M0.4: {step_4}")
        print(f"[INFO] step_5 M0.5: {step_5}")
        print(f"[INFO] step_6 M0.6: {step_6}")

        print(f"[INFO] light_DP Q0.0: {light_dp}")
        print(f"[INFO] finish_ligth(test) Q0.4: {finish_light}")
        print(f"[INFO] v5 Q0.5: {v5}")
        print(f"[INFO] v6 Q0.6: {v6}")
        print(f"[INFO] v9 Q0.7: {v9}")

        print("\n[INFO] Writing Tag_1 M10.0 = FALSE")
        write_m_bit(plc, 10, 0, False)
        time.sleep(0.5)

        print("[INFO] Writing Tag_1 M10.0 = TRUE")
        write_m_bit(plc, 10, 0, True)
        time.sleep(1.0)

        step_1_after_start = read_m_bit(plc, 0, 1)
        light_dp_after_start = read_q_bit(plc, 0, 0)

        print(f"[INFO] step_1 after start: {step_1_after_start}")
        print(f"[INFO] light_DP after start: {light_dp_after_start}")

        print("[INFO] Writing Tag_1 M10.0 = FALSE")
        write_m_bit(plc, 10, 0, False)

        print("\n[PASS] Snap7 read/write test completed")

    except Exception as e:
        print("\n[FAIL] Snap7 PLC connection test failed")
        print(f"[ERROR] {e}")

    finally:
        try:
            plc.disconnect()
            print("[INFO] Disconnected from PLC")
        except Exception:
            pass

        print("\n==============================")
        print("PLC SNAP7 CONNECTION TEST COMPLETE")
        print("==============================\n")


if __name__ == "__main__":
    test_plc_connection()
