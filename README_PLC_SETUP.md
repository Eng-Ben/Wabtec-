PLC Setup Guide

System Overview

The prototype uses:

- Siemens S7-1200 PLC
- Raspberry Pi 5
- Snap7 communication
- TIA Portal Ladder logic

The Raspberry Pi communicates directly with the PLC using Siemens S7 communication over Ethernet.

PLC Network Settings

The PLC IP address, rack, and slot configuration used in the prototype environment must match:

- the TIA Portal hardware configuration
- the values configured inside plc_client.py

Example prototype configuration:

PLC_IP = "192.168.x.x"
PLC_RACK = 0
PLC_SLOT = 1

These values may vary depending on:

- the company network setup
- the PLC hardware configuration
- the final Raspberry Pi deployment environment

TIA Portal Configuration

Inside TIA Portal:

1. Open Device Configuration
2. Select the PLC CPU
3. Open:

Properties → Protection & Security

Enable:

Permit access with PUT/GET communication from remote partner

Recommended access level:

Full access

Download both:

- hardware configuration
- software changes

to the PLC after configuration updates.

PLC Start Logic

The PLC sequence is started using:

- Physical start button connected to %I0.0
- Raspberry Pi arm signal %M10.0

The PLC only starts when:

- the Raspberry Pi has armed the system
- the operator presses the physical start button

The Raspberry Pi does not directly force the PLC sequence.

Relevant PLC Memory Bits

Step states:

M0.1 = step_1
M0.2 = step_2
M0.3 = step_3
M0.4 = step_4
M0.5 = step_5
M0.6 = step_6

Raspberry Pi arm signal:

M10.0 = Tag_1

Relevant outputs:

Q0.0 = light_DP
Q0.4 = finish_light
Q0.5 = v5
Q0.6 = v6
Q0.7 = v9

Physical start button:

I0.0 = button_start

Raspberry Pi Setup

Activate virtual environment:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the application:

python3 main.py

Testing PLC Communication

Run:

python3 plc_connection_test.py

Expected:

- successful Snap7 connection
- successful read/write of PLC bits
- monitoring of step states and outputs

Code Transfer to Raspberry Pi

Code can be transferred to the Raspberry Pi using tools such as:

- rsync
- SCP
- Git
- Visual Studio Code Remote SSH

The exact Raspberry Pi username, hostname, and IP address depend on the final deployment environment and network configuration.

Exporting PDF Reports

Generated PDF reports are stored in:

reports/

Reports can be transferred from the Raspberry Pi using:

- SCP
- rsync
- USB transfer
- network file sharing
