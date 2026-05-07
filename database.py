import sqlite3
from datetime import datetime

DB_PATH = "data/pressure_data.db" # Database file location

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS pressure_log (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp TEXT,
                   pressure_actual REAL,
                   pressure_setpoint REAL,
                   valve_output REAL,
                   alarm_status INTEGER
                   ) 
                   """)
    
    conn.commit()
    conn.close()


def save_data(data):
        # Create the table if it does not already exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO pressure_log (
                       timestamp,
                       pressure_actual,
                       pressure_setpoint,
                       valve_output,
                       alarm_status
                       ) VALUES (?, ?, ?, ?, ?
                       )""", (
                           datetime.now().isoformat(),      # Current timestamp in ISO format
                           data["pressure_actual"],         # Measured pressure 
                           data["pressure_setpoint"],       # Target pressure
                           data["valve_output"],            # Control signal
                           data["alarm_status"]             # Alarm Flag
                       ))
        conn.commit()
        conn.close()

def read_all():
    # Retrieve all stored pressure data from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pressure_log")
    rows = cursor.fetchall()

    conn.close()
    return rows