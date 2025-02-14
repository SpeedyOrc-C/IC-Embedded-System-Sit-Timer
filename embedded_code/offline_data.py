import os
from http_api import post_stand_data, post_sit_data
import time

OFFLINE_FILE = "offline_data.txt"

def store_offline_data(event_name, time_now):
    print("No network connection, storing offline event for", event_name)
    record = f"{event_name} {time_now}\n"  # simple record with event name and timestamp
    try:
        with open(OFFLINE_FILE, "a") as f:
            f.write(record)
    except Exception as e:
        print("Error saving offline data:", e)
  
def process_offline_data():
    """
    When the network is available, read the offline storage file and post each event.
    If some events are processed successfully and others are not,
    rewrite the file with only the unprocessed events.
    """
    if os.path.exists(OFFLINE_FILE):
        try:
            with open(OFFLINE_FILE, "r") as f:
                lines = f.readlines()
            remaining_lines = []
            success = True
            for line in lines:
                if not success:
                      print("Network connection problem encountered during offline processing. Stopping further processing.")
                      # Add the current event and the rest to remaining_lines.
                      remaining_lines.append(line)
                      continue
                parts = line.strip().split()
                if not parts:
                    continue
                event_name = parts[0]
                time_now = int(parts[1])
                print("Processing offline event:", event_name)
                success = False
                if event_name == "Standup":
                    success = post_stand_data(time_now)
                elif event_name == "Sitdown":
                    success = post_sit_data(time_now)
                # If posting fails, keep the event record
                if success == 202:
                    print(f"duplicate event: {event_name} {time_now}")
                if success == 400 or success == 404 or success == -1:
                    print(f"Failed to process offline event: {event_name}")
                    remaining_lines.append(line)
            if remaining_lines:
                with open(OFFLINE_FILE, "w") as f:
                    f.writelines(remaining_lines)
                print("Some offline events remain unprocessed.")
            else:
                os.remove(OFFLINE_FILE)
                print("All offline events processed successfully.")
        except Exception as e:
            print("Error processing offline data:", e)