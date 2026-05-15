Wabtec Valve Pressure Test System

Overview

This project is a prototype automated valve pressure inspection system developed using:

* Raspberry Pi 5
* Siemens PLC
* OPC UA communication
* Python
* SQLite database
* PDF report generation

The system is designed to simulate and later control a real industrial pressure test bench for pneumatic train brake valves.

The Raspberry Pi acts as the main controller and operator interface.
It selects test programs, communicates with the PLC through OPC UA, logs pressure data, evaluates pass/fail conditions, and generates inspection reports in PDF format.

System Workflow

1. Operator scans or enters a valve ID
2. Raspberry Pi identifies the correct test program
3. Test parameters are sent to the PLC through OPC UA
4. PLC executes the pressure test
5. Pressure values are monitored during the test
6. Measured data is stored in SQLite database
7. Pass/Fail result is evaluated
8. PDF inspection report is generated automatically

Technologies Used

Technology	Purpose
Python	Main application logic
asyncua	OPC UA communication
SQLite	Local test result database
matplotlib	Pressure graph generation
reportlab	PDF report generation
Raspberry Pi 5	Main controller
Siemens PLC	Industrial control system
OPC UA	Communication between PLC and Raspberry Pi

Project Structure

Wabtec/
│
├── assets/
│   └── wabtec_logo.png
│
├── data/
│   └── pressure_data.db
│
├── reports/
│   └── generated PDF reports
│
├── test_programs/
│   ├── valve_tests.json
│   └── valve_map.json
│
├── main.py
├── plc_client.py
├── opc_server.py
├── database.py
├── report.py
├── input_reader.py
├── config.py
├── requirements.txt
└── README.md

Main Components

main.py

Main application controller.

Responsibilities:

* Reads valve input
* Selects correct test program
* Starts PLC test
* Saves results
* Generates PDF reports

opc_server.py

Simulated OPC UA PLC server.

Responsibilities:

* Simulates PLC variables
* Simulates pressure behavior
* Handles test execution
* Updates OPC UA nodes

plc_client.py

OPC UA client communication.

Responsibilities:

* Connects to PLC
* Sends test parameters
* Starts tests
* Reads measured values
* Collects pressure series data

database.py

SQLite database handling.

Responsibilities:

* Creates database
* Saves inspection results
* Reads stored test data

report.py

PDF report generator.

Responsibilities:

* Generates pressure graphs
* Creates inspection PDFs
* Displays pass/fail result
* Adds timestamps and operator information

OPC UA Variables

Variable	Description
StartTest	Starts PLC test
SelectedProgramID	Active test program
PressureSetpoint	Desired pressure
MinPressure	Minimum accepted pressure
MaxPressure	Maximum accepted pressure
TestDuration	Test runtime
MeasuredPressure	Live pressure reading
TestPassed	Pass/Fail result
AlarmStatus	Alarm state
TestDone	Test complete signal

Running the System

1. Activate Python virtual environment

source venv/bin/activate

2. Start OPC UA server

python opc_server.py

3. Start main application

Open a second terminal:

source venv/bin/activate
python main.py

Required Python Packages

Install dependencies:

pip install -r requirements.txt

Main dependencies:

* asyncua
* matplotlib
* reportlab
* pandas
* pillow

Current Features

* OPC UA communication
* Valve program selection
* Simulated PLC pressure control
* Pressure graph generation
* SQLite logging
* PDF inspection reports
* Operator name support
* Pass/Fail evaluation
* Test ID generation

Planned Improvements

* Real Siemens PLC integration
* RFID scanner support
* Real pressure sensors
* Live dashboard
* Historical trend analysis
* Alarm handling
* Multiple valve test programs
* State machine implementation
* Web interface
* Automatic report export

Example Report Content

Generated PDF reports include:

* Test ID
* Operator name
* Valve type
* Program ID
* Pressure limits
* Measured pressure
* Pass/Fail result
* Timestamp
* Pressure graph

Authors

Developed as part of the Wabtec EPS engineering project.

Prototype developed for automated industrial valve pressure testing.