#OPC_SERVER_URL = "opc.tcp://192.168.0.1:4840"

# OPC_NODES = {
#     # Pi writes this to start the PLC test sequence
#     "start_test": 'ns=3;s="Tag_1"',

#     # Pi reads this to know when PLC sequence is finished
#     "test_done": 'ns=3;s="finish_ligth(test)"',

#     # These are not real PLC pressure values yet
#     # Keep simulated in Python for now
#     "pressure_simulation_mdp": 'ns=3;s="pressure_simulation_MDP"',
#     "pressure_simulation_mcf": 'ns=3;s="pressure_simulation_MCF"',

#     # Optional readouts
#     "step_1": 'ns=3;s="step_1"',
#     "step_2": 'ns=3;s="step_2"',
#     "step_3": 'ns=3;s="step_3"',
#     "step_4": 'ns=3;s="step_4"',
#     "step_5": 'ns=3;s="step_5"',
#     "step_6": 'ns=3;s="step_6"',

#     "v5": 'ns=3;s="v5"',
#     "v6": 'ns=3;s="v6"',
#     "v9": 'ns=3;s="v9"',
# }

OPC_SERVER_URL = "opc.tcp://localhost:4840"

OPC_NODES = {
    "start_test": "ns=2;i=2",
    "selected_program_id": "ns=2;i=3",
    "pressure_setpoint": "ns=2;i=4",
    "min_pressure": "ns=2;i=5",
    "max_pressure": "ns=2;i=6",
    "test_duration": "ns=2;i=7",
    "test_done": "ns=2;i=8",
    "measured_pressure": "ns=2;i=9",
    "test_passed": "ns=2;i=10",
    "alarm_status": "ns=2;i=11"
}