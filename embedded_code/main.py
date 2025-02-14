import requests
import time
import threading
from ultra_sensor import get_distance
from flex_sensor import read_flex_sensor
from http_api import post_sit_data, post_stand_data, get_pairing_code, is_paired, get_offline_mode
from display import init_display, display_text
from offline_data import store_offline_data, process_offline_data

# global variables, to keep track of sit time
start_sit_time = -1
pairing_now = False

def pairing():
    global pairing_now

    json = get_pairing_code()
    if json:
        print("Pairing code Fetched. ", "code: ", json['code'], "id: ", json['id'])
        id, code = json['id'], json['code']
        with open("device_id.txt", "w") as f:
            f.write(id)
        pairing_now = True
        while True:
            display_text(code.upper())
            is_paired_res = is_paired()
            if is_paired_res == 200:
                print("Pairing successful")
                display_text("----")
                time.sleep(5)
                display_text("    ")
                pairing_now = False
                return
            if is_paired_res == -1:
                print("No network connection available for pairing. offline mode enabled.")
                pairing_now = False
                return
            # is_paired_res == 404
            print("Pairing not done, will recheck in 5 seconds")
            time.sleep(5)
    else:
        print("Pairing failed, will try again in 5 seconds")
        time.sleep(5)
        pairing()

# display sit time on screen
def display_sitting_time():
    # express in seconds
    time_elapsed = time.time() - start_sit_time
    if start_sit_time == -1:
        display_text("    ")
    elif time_elapsed >= 1800:
        display_text("UPUP")
    else:
        # convert time to four digit string convert to time format
        string = time.strftime("%M%S", time.gmtime(time_elapsed))
        display_text(string)

def check_error_voltage(flex_voltage) -> bool:
    if flex_voltage == -1 or (flex_voltage > 26300 and flex_voltage < 26400):
        print("Error in reading flex sensor")
        return True
    return False

def check_error_ultra(ultra_distance) -> bool:
    if ultra_distance == -1 or ultra_distance > 1000:
        print("Error in reading ultra sensor")
        return True
    return False


# post data to server
def post_data_stand_sit_data(event_name, post_func):
    global start_sit_time
    time_now = int(time.time())
    if event_name == "Standup":
            start_sit_time = -1
    else:
        # if sitdown event is detected, start the timer only if it is not already started
        if start_sit_time == -1:
            start_sit_time = time_now
    if not get_offline_mode():
        response_code = post_func(time_now)
        print("Response code: ", response_code)
        # if response code is 400 or 404, store the data in offline mode
        if response_code == 400 or response_code == 404 or response_code == -1:
            store_offline_data(event_name, time_now)
    else:
        store_offline_data(event_name, time_now)

def detect_event(flex_voltage, ultra_distance, flex_cond, ultra_cond, event_name, post_func):
    """
    If both sensors are valid, event is detected only if both conditions are met.
    If one sensor is in error, then the event is determined solely by the valid sensor.
    """
    flex_ok = not check_error_voltage(flex_voltage)
    ultra_ok = not check_error_ultra(ultra_distance)
    
    if flex_ok and ultra_ok:
        if flex_cond(flex_voltage) and ultra_cond(ultra_distance):
            print(f"{event_name} detected using both sensors")
            post_data_stand_sit_data(event_name, post_func)
            return True
    elif flex_ok:
        if flex_cond(flex_voltage):
            print(f"{event_name} detected using flex sensor only")
            post_data_stand_sit_data(event_name, post_func)
            return True
    elif ultra_ok:
        if ultra_cond(ultra_distance):
            print(f"{event_name} detected using ultrasound sensor only")
            post_data_stand_sit_data(event_name, post_func)
            return True
    return False


def check_standup(flex_voltage, ultra_distance) -> bool:
    """
    Standup is detected if:
    - Both sensors valid and:
        flex sensor value is between 14000 and 15500, AND
        ultrasonic distance is between 15 and 150.
    - If one sensor errors, then the other sensor must satisfy its threshold.
    """
    
    return detect_event(
        flex_voltage,
        ultra_distance,
        flex_cond=lambda v: 14000 < v < 15500,
        ultra_cond=lambda d: 15 < d < 150,
        event_name="Standup",
        post_func=post_stand_data
    )

def check_sitdown(flex_voltage, ultra_distance) -> bool:
    """
    Sitdown is detected if:
    - Both sensors valid and:
        flex sensor value is between 16000 and 20000 OR between 10000 and 13500, AND
        ultrasonic distance is less than 15.
    - If one sensor errors, then the other sensor must satisfy its threshold.
    """
    
    return detect_event(
        flex_voltage,
        ultra_distance,
        flex_cond=lambda v: (16000 < v < 22000) or (10000 < v < 13500),
        ultra_cond=lambda d: d < 15,
        event_name="Sitdown",
        post_func=post_sit_data
    )

def get_current_value() -> tuple:
    flex_voltage = read_flex_sensor()
    ultra_distance = get_distance()
    return flex_voltage, ultra_distance

def update_display_thread():
    global pairing_now
    """Updates the sitting time display every second."""
    while True:
        # if not pairing, display the sitting time
        if not pairing_now:
            display_sitting_time()
        time.sleep(1)


def main():
    init_display()
    display_text("    ")
    if is_paired() == 404:
        pairing()
    print("start monitoring")
    
    # Start the display update thread (daemon thread so it stops when main exits)
    display_thread = threading.Thread(target=update_display_thread, daemon=True)
    display_thread.start()
    
    while True:
        is_paired_res = is_paired()
        print("Is paired: ", is_paired_res)
        if is_paired_res != -1: # have network connection
            if is_paired_res == 404: # not paired
                # stop thread if not paired
                print("Network available but device not paired. Initiating pairing sequence...")
                pairing()
            process_offline_data()
        flex_voltage, ultra_distance = get_current_value()
        print("Flex Voltage: ", flex_voltage, "Ultra Distance: ", ultra_distance)
        
        check_standup(flex_voltage, ultra_distance)
        check_sitdown(flex_voltage, ultra_distance)

        time.sleep(1)

if __name__ == "__main__":
    main()

