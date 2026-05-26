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
            valve_id TEXT,
            program_id INTEGER,
            valve_type TEXT,
            pressure_setpoint REAL,
            measured_pressure REAL,
            min_pressure REAL,
            max_pressure REAL,
            test_duration_seconds REAL,
            alarm_status INTEGER,
            result TEXT
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pressure_samples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id TEXT,
        timestamp TEXT,
        sample_time REAL,
        pressure_value REAL
    )
""")

    conn.commit()
    conn.close()


def save_test_result(valve_id, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inspection_results (
            timestamp,
            valve_id,
            program_id,
            valve_type,
            pressure_setpoint,
            measured_pressure,
            min_pressure,
            max_pressure,
            test_duration_seconds,
            alarm_status,
            result
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            datetime.now().isoformat(),
            valve_id,
            result["program_id"],
            result["valve_type"],
            result["pressure_setpoint"],
            result["measured_pressure"],
            result["min_pressure"],
            result["max_pressure"],
            result["test_duration_seconds"],
            result["alarm_status"],
            result["result"],
        ),
    )

    conn.commit()
    conn.close()


def save_pressure_samples(test_id, pressure_series):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for sample in pressure_series:
        cursor.execute(
            """
            INSERT INTO pressure_samples (
                test_id,
                timestamp,
                sample_time,
                pressure_value
            ) VALUES (?, ?, ?, ?)
        """,
            (test_id, datetime.now().isoformat(), sample["time"], sample["pressure"]),
        )

    conn.commit()
    conn.close()


def read_pressure_samples(test_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sample_time, pressure_value
        FROM pressure_samples
        WHERE test_id = ?
        ORDER BY sample_time
    """,
        (test_id,),
    )

    rows = cursor.fetchall()

    conn.close()
    return rows
