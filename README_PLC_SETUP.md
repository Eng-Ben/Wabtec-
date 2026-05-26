PLC Setup Guide

Purpose

This document describes the steps needed to connect the Raspberry Pi Python system to the real Siemens PLC using OPC UA.

The goal is to replace the simulated OPC server with the real PLC OPC UA server.

Current Development Setup

During development, the system uses:

Python main.py
↓
Local simulated OPC UA server
↓
opc_server.py

This is used when:

USE_REAL_PLC = False

Final PLC Setup

When connected to the real Siemens PLC, the system should use:

Python main.py
↓
Raspberry Pi OPC UA client
↓
Siemens PLC OPC UA server
↓
Switchboard simulation

This is used when:

USE_REAL_PLC = True

Network Setup

The Raspberry Pi should use:

WiFi → SSH access from Mac
Ethernet → PLC communication

Example network:

PLC IP: 192.168.0.1
Raspberry Pi eth0: 192.168.0.20
Mac/Pi WiFi: 192.168.1.x

Step 1: Check Raspberry Pi Network

On Raspberry Pi:

ip addr

Confirm:

wlan0 has WiFi IP
eth0 has PLC-network IP

Step 2: Test PLC Network Contact

On Raspberry Pi:

ping 192.168.0.1

Expected:

64 bytes from 192.168.0.1

Stop ping:

CTRL + C

If ping fails, check:

- Ethernet cable
- PLC power
- PLC IP address
- Raspberry Pi eth0 IP
- subnet settings

Step 3: Enable OPC UA On Siemens PLC

In TIA Portal:

Device Configuration
→ OPC UA
→ Enable OPC UA Server

Check:

- OPC UA server enabled
- port 4840 active
- tags are exposed
- read/write access allowed

Step 4: Required PLC Tags

Minimum required tags:

| Python name | PLC tag                    | Purpose                      |
| ----------- | -------------------------- | ---------------------------- |
| start_test  | Tag_1 / %M10.0             | Start test from Raspberry Pi |
| test_done   | finish_ligth(test) / %Q0.4 | PLC test finished            |
| step_1      | step_1 / %M0.1             | Optional sequence state      |
| step_2      | step_2 / %M0.2             | Optional sequence state      |
| step_3      | step_3 / %M0.3             | Optional sequence state      |
| step_4      | step_4 / %M0.4             | Optional sequence state      |
| step_5      | step_5 / %M0.5             | Optional sequence state      |
| step_6      | step_6 / %M0.6             | Optional sequence state      |
| v5          | v5 / %Q0.5                 | Optional valve output        |
| v6          | v6 / %Q0.6                 | Optional valve output        |
| v9          | v9 / %Q0.7                 | Optional valve output        |

Step 5: Find OPC UA Node IDs

Use UaExpert on the TIA/PLC computer.

Connect to:

opc.tcp://192.168.0.1:4840

Find the real Node IDs for:

Tag_1
finish_ligth(test)
step_1
step_2
step_3
step_4
step_5
step_6
v5
v6
v9

Example Node ID:

ns=3;s="Tag_1"

Note: actual Node IDs may be different. Always copy them from UaExpert.

Step 6: Update Real PLC Config

Open:

config_files/real_plc.py

Update:

OPC_SERVER_URL = "opc.tcp://192.168.0.1:4840"

Then update all Node IDs:

OPC_NODES = {
"start_test": 'REAL_NODE_ID_HERE',
"test_done": 'REAL_NODE_ID_HERE',
}

Step 7: Enable Real PLC Mode

Open:

config.py

Set:

USE_REAL_PLC = True

Important:

When using the real PLC, do not run:

python opc_server.py

The Siemens PLC is now the OPC UA server.

Step 8: Run Connection Test First

Before running the full system, run:

python plc_connection_test.py

Expected output:

[PASS] Connected to OPC server
[PASS] Found start_test node
[PASS] Found test_done node
[PASS] Read TestDone value
[PASS] Successfully wrote StartTest=False

If this fails, do not run main.py yet.

Fix:

- network
- OPC UA settings
- Node IDs
- tag permissions

Step 9: Run Main System

When connection test passes:

python main.py

Expected flow:

Scan or type valve ID
Operator name
Start PLC test
Wait for TestDone
Generate PDF report
Save database result

Step 10: Report Output

PDF reports are saved in:

reports/

Database is saved in:

data/pressure_data.db

Troubleshooting

Cannot connect to OPC server

Check:

- PLC IP
- Ethernet cable
- Raspberry Pi eth0 IP
- OPC UA enabled
- port 4840
- firewall/security settings

BadUserAccessDenied

Usually means:

- tag is not writable
- OPC user lacks permission
- trying to write to physical input
- PLC security setting blocks write access

Use memory bit or DB tag for writable commands.

BadNodeIdUnknown

Usually means:

- wrong Node ID
- tag not exposed through OPC UA
- namespace index changed
- typo in config

Use UaExpert to confirm.

Test never finishes

Check:

- test_done Node ID
- PLC sequence reaches finish state
- finish_ligth(test) actually turns TRUE
- Python timeout setting

Important Notes

The PLC is currently connected to a switchboard simulation.

This means:

- no real pressure sensor is used
- pressure is simulated in Python
- PLC provides sequence/state logic
- Raspberry Pi generates simulated pressure curves
- reports are proof-of-concept inspection reports

Final System Architecture

Mac
↓ SSH / VS Code
Raspberry Pi
↓ Ethernet / OPC UA
Siemens PLC
↓
Switchboard simulation

Before PLC Test Day Checklist

- Raspberry Pi boots
- SSH from Mac works
- Python venv works
- requirements installed
- project copied to Raspberry Pi
- plc_connection_test.py works in simulation
- main.py works in simulation
- config_files/real_plc.py ready
- PLC IP known
- OPC UA enabled
- UaExpert installed
- Node IDs found
- USE_REAL_PLC = True
