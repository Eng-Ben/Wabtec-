def read_valve_code(valid_codes=None):
    print()
    print("Available valve/test programs:")

    if valid_codes:
        for code in valid_codes:
            print(f"  - {code}")

    print()
    return input("Scan or type valve ID: ").strip()