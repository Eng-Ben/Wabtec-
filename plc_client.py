import random

def read_plc_data():
    return {
        "pressure_actual" : round(random.uniform(4.5, 6.5), 2),
        "pressure_setpoint" : 6.0,
        "valve_output" : round(random.uniform(20, 80), 1),
        "alarm_status" : 0
    }