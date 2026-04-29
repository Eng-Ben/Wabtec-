import sqlite3
from datetime import datetime

DB_PATH = "data/pressure_data.db"

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
                           datetime.now().isoformat(),
                           data["pressure_actual"],
                           data["pressure_setpoint"],
                           data["valve_output"],
                           data["alarm_status"]
                       ))
        conn.commit()
        conn.close()

def read_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pressure_log")
    rows = cursor.fetchall()

    conn.close()
    return rows