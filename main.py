import time
from plc_client import read_plc_data
from database import init_db, save_data

LOG_INTERVAL_SECONDS = 5

init_db()

print("Pressure logging started. Press CTRL+C to stop.")

try:
    while True:
        data = read_plc_data()
        save_data(data)
        print("Saved:", data)
        time.sleep(LOG_INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("Logging stopped.")

    #Stop the program gracefully on CTRL+C