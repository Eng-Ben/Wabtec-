import time
from plc_client import read_plc_data
from database import init_db, save_data

LOG_INTERVAL_SECONDS = 5 # Time inbetween each data read (Seconds)

# initialize the database and create the necessary tables if they don't exist
init_db()

print("Pressure logging started. Press CTRL+C to stop.")

try:
    # Continuously read data from the PLC and save it to the database at regular intervals
    while True:
        data = read_plc_data()
        save_data(data)
        print("Saved:", data)
        time.sleep(LOG_INTERVAL_SECONDS)

except KeyboardInterrupt:
    # Handle the CTRL+C signal to stop the logging gracefully
    print("Logging stopped.")