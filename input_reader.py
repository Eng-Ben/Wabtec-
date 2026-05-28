def read_valve_code(valid_codes=None):
    print()
    print("Available valve/test programs:")

    # Displays all available valve IDs loaded from valve_map.json.
    # This helps the operator select a valid test program.
    if valid_codes:
        for code in valid_codes:
            print(f"  - {code}")

    print()

    # The operator can either manually type the valve ID
    # or later replace this with a barcode/RFID scanner input.
    return input("Scan or type valve ID: ").strip()
