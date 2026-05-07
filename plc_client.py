import random

# Simulated PLC client that generates random pressure data for testing purposes
def read_plc_data():
    return {
        # Simulates measured pressure between 4.5 and 6.5 bar, rounded to 2 decimal places
        "pressure_actual" : round(random.uniform(4.5, 6.5), 2),

        # Simulates target pressure at 6.0 bar
        "pressure_setpoint" : 6.0,

        # Simulates valve output between 20% and 80%, rounded to 1 decimal place
        "valve_output" : round(random.uniform(20, 80), 1),

        # Simulates alarm status with a 10% chance of being active (1) and 90% chance of being inactive (0)
        "alarm_status" : 0
    }