````markdown
# Pressure Control and Data Logging System

## Project Description
This project is a pressure monitoring and control system using an Omron PLC and a Raspberry Pi 5.  
The PLC is responsible for handling pressure regulation and control logic, while the Raspberry Pi collects data, stores measurements in a database, and generates reports.

The system is designed to:
- Monitor pressure values
- Store pressure measurements
- Simulate PLC communication during development
- Generate datasets for analysis and reporting
- Prepare for future PLC integration



# System Overview

```text
Pressure Sensor → Omron PLC → Control Logic
                           ↓
                    Raspberry Pi 5
                           ↓
                    SQLite Database
                           ↓
                      PDF Reports
```



# Technologies Used

- Python
- SQLite
- Raspberry Pi 5
- Omron PLC
- VS Code

Python libraries:
- sqlite3
- pandas
- matplotlib
- reportlab



# Project Structure

```text
Wabtec-/
│
├── main.py
├── plc_client.py
├── database.py
├── report.py
├── config.py
├── requirements.txt
│
├── data/
│   └── pressure_data.db
│
└── venv/
```



# File Descriptions

## main.py
Main application loop responsible for:
- Reading PLC data
- Saving data to the database
- Running continuous logging

## plc_client.py
Simulates PLC communication during development.
Will later be replaced with real Omron PLC communication.

## database.py
Handles:
- Database creation
- Data storage
- Reading stored measurements

## report.py
Will generate graphs and PDF reports from stored data.

## config.py
Used for configurable project settings.



# Current Features

- Simulated PLC pressure data
- SQLite database logging
- Continuous data collection
- Timestamped measurements



# Future Improvements

- Real Omron PLC communication
- Live pressure visualization
- PDF report generation
- Alarm handling
- PID monitoring
- Real sensor integration



# Example Logged Data

```python
{
    "pressure_actual": 5.84,
    "pressure_setpoint": 6.0,
    "valve_output": 42.7,
    "alarm_status": 0
}
```



# How to Run the Project

## Activate virtual environment

```bash
source venv/bin/activate
```

## Run the logger

```bash
python main.py
```

Stop logging with:

```text
CTRL + C
```



# Notes

The current PLC communication is simulated using randomly generated values.  
The simulation will later be replaced with real Omron PLC communication once the hardware and PLC model are available.
````
