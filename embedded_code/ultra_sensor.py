import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG = 23  # Trigger pin (output)
ECHO = 24  # Echo pin (input)

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Send ultrasonic pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Send a 10µs pulse
    GPIO.output(TRIG, False)
    
    # Timeouts in seconds (adjust as needed)
    timeout = 0.04

    # Wait for the Echo pin to go HIGH (sound wave sent)
    start_time = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - start_time > timeout:
            # print("Timeout waiting for ECHO to go HIGH")
            return -1
    pulse_start = time.time()

    # Wait for the Echo pin to go LOW (sound wave received)
    while GPIO.input(ECHO) == 1:
        if time.time() - pulse_start > timeout:
            # print("Timeout waiting for ECHO to go LOW")
            return -1
    pulse_end = time.time()

    duration = pulse_end - pulse_start

    # Calculate the distance (in cm)
    distance = (duration * 34300) / 2  # Speed of sound = 343 m/s, divided by 2 for round-trip
    return distance


if __name__ == "__main__":
    try:
        while True:
            print("Measuring distance...")
            dist = get_distance()
            print(f"Distance: {dist:.2f} cm")  # Print measured distance
            time.sleep(1)  # Wait 1 second before the next measurement
    except KeyboardInterrupt:
        GPIO.cleanup()  # Release GPIO resources when script is interrupted