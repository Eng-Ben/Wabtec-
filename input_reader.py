def read_valve_code():
    # Reads valve code from keyboard, barcode scanner, or RFID reader. For now, we will just read from the keyboard.
    return input("Scan or type valve ID: ").strip().upper()