Wabtec Valve Test Bench Prototype

Overview

This project is a prototype automation system developed for a pneumatic valve test bench in collaboration with Wabtec.

The system combines:

- Siemens S7-1200 PLC
- Raspberry Pi 5
- Python supervisory software
- Snap7 PLC communication
- SQLite logging
- Automatic PDF report generation

The PLC handles the deterministic sequence logic and output control, while the Raspberry Pi handles:

- valve program selection
- PLC communication
- test supervision
- data logging
- PDF report generation

The project was developed as part of an engineering student project focused on industrial automation and digital test traceability.

Current Prototype Functionality

The current prototype is capable of:

- Connecting to a Siemens PLC using Snap7
- Starting and monitoring a PLC sequence
- Selecting valve programs dynamically from JSON files
- Logging sequence progression
- Storing test data in SQLite
- Generating PDF inspection reports automatically

The PLC sequence is started using a physical push button connected to the PLC input system, while the Raspberry Pi acts as the supervisory layer.

Project Structure

Main files:

- main.py
  Main application entry point
- plc_client.py
  Snap7 PLC communication and sequence monitoring
- database.py
  SQLite database handling
- report.py
  PDF report generation
- input_reader.py
  Operator valve/program selection
- test_programs/valve_map.json
  Maps operator input to PLC test programs
- test_programs/valve_tests.json
  Contains test parameters and configuration

Requirements

Python version:

- Python 3.13+

Install required packages:

pip install -r requirements.txt

Running the Project

Activate virtual environment:

source venv/bin/activate

Run the application:

python3 main.py

The operator can then:

1. Select a valve ID
2. Start the PLC sequence using the physical start button
3. Wait for sequence completion
4. Generate a PDF inspection report automatically

PLC Communication

The Raspberry Pi communicates directly with the Siemens S7-1200 PLC using the Snap7 library.

The PLC:

- executes the Ladder logic
- controls outputs
- manages step transitions

The Raspberry Pi:

- monitors PLC states
- logs sequence data
- generates reports

Communication is performed through Siemens memory bits and output states.

Report Generation

After a completed sequence:

- the test result is stored in SQLite
- a PDF report is generated automatically
- the report includes:
  - valve information
  - test parameters
  - PLC phases detected
  - sequence timing
  - pressure graph structure

Reports are saved in:

reports/

Future Improvements

Planned future improvements include:

- Real pressure sensor integration
- RFID/barcode scanning
- Multiple valve program support
- Expanded PLC sequence library
- Improved industrial HMI integration
- Real-time pressure plotting
