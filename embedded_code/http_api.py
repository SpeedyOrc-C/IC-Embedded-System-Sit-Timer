import requests
import os
import time
device_id = ""

offline_mode = False  # Global flag for offline mode

def get_offline_mode() -> bool:
    return offline_mode

def get_pairing_code() -> bool:
    global device_id, offline_mode
    offline_mode = False # Reset offline mode flag
    url = "http://while-you-seat.speedyorc-chen.site/api/device/pairing"
    try:
        # Use a correct JSON payload (dictionary) rather than a string
        response = requests.post(url, json={"id": "12121"}, timeout=3)
        response.raise_for_status()
        data = response.json()
        device_id = data.get("id")
        return data
    except requests.exceptions.Timeout or requests.exceptions.ConnectionError as e:
        print("no network connection, switch to offline mode")
        offline_mode = True
        return -1
    except requests.exceptions.RequestException as e:
        print("get_pairing_code failed:", e)
        return False

# 200 for success, 202 for duplicate, 400 for bad request, 404 for not found, -1 for other errors
def post_sit_data(time) -> int:
    global offline_mode
    offline_mode = False # Reset offline mode flag
    if device_id == "":
        raise ValueError("device_id is empty in post_sit_data")
    url = f"http://while-you-seat.speedyorc-chen.site/api/device/{device_id}/log/yes/{time}"
    try:
        response = requests.post(url, timeout=3)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.Timeout or requests.exceptions.ConnectionError as e:
        print("no network connection, switch to offline mode")
        offline_mode = True
        return -1
    except requests.exceptions.RequestException as e:
        print("post_sit_data failed:", e)
        if hasattr(e, 'response') and e.response is not None:
            return e.response.status_code
        return -1

def post_stand_data(time) -> int:
    global offline_mode
    offline_mode = False # Reset offline mode flag
    if device_id == "":
        raise ValueError("device_id is empty in post_stand_data")
    url = f"http://while-you-seat.speedyorc-chen.site/api/device/{device_id}/log/no/{time}"
    try:
        response = requests.post(url, timeout=3)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.Timeout or requests.exceptions.ConnectionError as e:
        print("no network connection, switch to offline mode")
        offline_mode = True
        return -1
    except requests.exceptions.RequestException as e:
        print("post_stand_data failed:", e)
        if hasattr(e, 'response') and e.response is not None:
            return e.response.status_code
        return -1

def is_paired()  -> int:
    global device_id, offline_mode
    offline_mode = False # Reset offline mode flag
    # Check if device_id is in memory; if not, check for the device_id.txt file.
    if device_id == "":
        if os.path.isfile("device_id.txt"):
            try:
                with open("device_id.txt", "r") as f:
                    device_id = f.read().strip()
            except Exception as e:
                print("Error reading device_id file:", e)
                return 404
        else:
            print("device_id.txt not found")
            return 404

    url = f"http://while-you-seat.speedyorc-chen.site/api/device/{device_id}"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.Timeout or requests.exceptions.ConnectionError as e:
        print("no network connection, switch to offline mode")
        offline_mode = True
        return -1
    except requests.exceptions.RequestException as e:
        print("is_paired failed:", e)
        if hasattr(e, 'response') and e.response is not None:
            return e.response.status_code
        return -1

if __name__ == "__main__":
    if device_id == "":
        if os.path.isfile("device_id.txt"):
            try:
                with open("device_id.txt", "r") as f:
                    device_id = f.read().strip()
            except Exception as e:
                print("Error reading device_id file:", e)
        else:
            print("device_id.txt not found")
    # content = get_pairing_code()
    print(post_sit_data(125))
    print(post_stand_data(1739325009))
    # print(content)