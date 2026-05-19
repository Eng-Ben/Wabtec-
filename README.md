Wabtec Valve Pressure Test System

Project Overview

This project is a proof-of-concept automated valve pressure testing system developed for Wabtec.

The system simulates and later integrates with a Siemens PLC to automate pneumatic valve testing procedures. A Raspberry Pi acts as the main controller and communicates with the PLC through OPC UA.

The system can:

- Start automated PLC test sequences
- Simulate or read pressure values
- Track PLC state machine phases
- Detect pressure hold/leak behaviour
- Generate PDF inspection reports
- Log valve test information
- Run in both simulation mode and real PLC mode

System Architecture

Main Components

- Raspberry Pi 5
- Siemens PLC
- OPC UA communication
- Python-based test client
- PDF report generation
- SQLite logging
- Simulated pneumatic process

Main Python Files

main.py
Starts and runs a selected valve test program.

plc_client.py
Handles OPC UA communication between Python and PLC/simulation server.

opc_server.py
Simulation server used before connecting to the real PLC.

report.py
Generates PDF inspection reports and pressure graphs.

config.py
Selects between simulation mode and real PLC mode.

config_files/simulation.py
OPC configuration for simulation environment.

config_files/real_plc.py
OPC configuration for real PLC environment.

reports/
Generated PDF reports and pressure graphs.

How The System Works

1. Python selects a valve test program
2. Raspberry Pi sends test parameters over OPC UA
3. PLC or simulation server starts sequence
4. PLC step states are monitored
5. Pressure values are collected
6. Test result is evaluated
7. PDF report is generated automatically

PLC State Machine

The system currently tracks these PLC phases:

- FILLING
- STABILIZING
- HOLDING
- VENTING
- FINISHING
- COMPLETE

Simulation Mode

Simulation mode allows the full software system to be tested without a real PLC.

Simulation includes:
- OPC UA server
- PLC state progression
- Pressure simulation
- Valve outputs
- PDF generation

To enable simulation mode:

Inside config.py:

USE_REAL_PLC = False

Then run:

python opc_server.py

In another terminal:

python main.py

Real PLC Mode

When connected to the Siemens PLC:

1. Configure OPC node IDs in:
   config_files/real_plc.py

2. Set:

USE_REAL_PLC = True

3. Start the Siemens OPC UA server

4. Run:

python main.py

Current Features

- OPC UA communication
- PLC state tracking
- Pressure hold test simulation
- Pressure graphs
- PDF inspection reports
- Raspberry Pi compatible setup
- Simulation/real PLC switching

Planned Improvements

- Real analog pressure input
- SQLite test logging
- Operator GUI
- Alarm handling
- Emergency stop handling
- Multiple valve test programs
- Automatic report archiving

Dependencies

Python libraries used:

- asyncua
- matplotlib
- reportlab

Install using:

pip install asyncua matplotlib reportlab

Example Test Types

Standard pressure test
Pressure hold / leak test

Hardware

Current development hardware:

- Raspberry Pi 5
- MacBook development environment
- Siemens PLC (planned integration)
- Pneumatic switchboard simulation setup

Project Status

Current status:
Software proof-of-concept completed.

The system successfully:
- Simulates PLC sequences
- Tracks PLC phases
- Generates reports
- Runs on Raspberry Pi
- Supports future Siemens PLC integration