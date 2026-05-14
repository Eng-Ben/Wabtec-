import sqlite3
from datetime import datetime

DB_PATH = "data/pressure_data.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspection_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            program_id INTEGER,
            valve_type TEXT,
            pressure_setpoint REAL,
            measured_pressure REAL,
            min_pressure REAL,
            max_pressure REAL,
            test_duration_seconds REAL,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_test_result(result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inspection_results (
            timestamp,
            program_id,
            valve_type,
            pressure_setpoint,
            measured_pressure,
            min_pressure,
            max_pressure,
            test_duration_seconds,
            result
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        result["program_id"],
        result["valve_type"],
        result["pressure_setpoint"],
        result["measured_pressure"],
        result["min_pressure"],
        result["max_pressure"],
        result["test_duration_seconds"],
        result["result"]
    ))

    conn.commit()
    conn.close()