USE_REAL_PLC = True

if USE_REAL_PLC:
    from config_files.real_plc import OPC_SERVER_URL, OPC_NODES
else:
    from config_files.simulation import OPC_SERVER_URL, OPC_NODES