
import RPi.GPIO as GPIO
import time

# Define GPIO pins for TM1637
CLK = 27  # Clock pin
DIO = 17  # Data pin

# TM1637 Command Set
ADDR_AUTO = 0x40  # Auto address increment mode
ADDR_FIXED = 0x44  # Fixed address mode
CMD_DISPLAY_ON = 0x88  # Display control command (with brightness)

# Character Map for 7-segment display (Common Anode)
SEGMENT_MAP = {
    '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F,
    '4': 0x66, '5': 0x6D, '6': 0x7D, '7': 0x07,
    '8': 0x7F, '9': 0x6F, 'A': 0x77, 'B': 0x7C,
    'C': 0x39, 'D': 0x5E, 'E': 0x79, 'F': 0x71,
    'U': 0x3E, 'P': 0x73, '-': 0x40, ' ': 0x00   
}

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIO, GPIO.OUT)

# TM1637 communication functions
def tm1637_start():
    """ Send TM1637 start signal """
    GPIO.output(DIO, True)
    GPIO.output(CLK, True)
    GPIO.output(DIO, False)
    GPIO.output(CLK, False)

def tm1637_stop():
    """ Send TM1637 stop signal """
    GPIO.output(CLK, False)
    GPIO.output(DIO, False)
    GPIO.output(CLK, True)
    GPIO.output(DIO, True)

def tm1637_write_byte(byte):
    """ Write 8-bit data to TM1637 """
    for i in range(8):
        GPIO.output(CLK, False)
        GPIO.output(DIO, (byte >> i) & 1)
        GPIO.output(CLK, True)

    # Acknowledge bit
    GPIO.output(CLK, False)
    GPIO.output(DIO, True)
    GPIO.output(CLK, True)
    GPIO.setup(DIO, GPIO.IN)
    time.sleep(0.00005)  # Wait for ACK
    GPIO.setup(DIO, GPIO.OUT)

def tm1637_set_brightness(level):
    """Set brightness level (0-7)"""
    if level < 0 or level > 7:
        level = 3  # Default to medium brightness
    tm1637_start()
    tm1637_write_byte(CMD_DISPLAY_ON | level)  # Brightness command
    tm1637_stop()

def tm1637_display(digits):
    """ Send a 4-digit number to the display """
    tm1637_start()
    tm1637_write_byte(ADDR_AUTO)  # Set auto-increment mode
    tm1637_stop()

    tm1637_start()
    tm1637_write_byte(0xC0)  # Start address

    # Send each digit
    for digit in digits:
        tm1637_write_byte(SEGMENT_MAP.get(digit, 0x00))  # Default to blank if unknown
    
    tm1637_stop()

def init_display():
    """ Initialize the display """
    tm1637_start()
    tm1637_write_byte(CMD_DISPLAY_ON | 0x0) # low brightness
    tm1637_stop()

def display_text(text):
    """ Display a 4-digit code """
    tm1637_display(text)


if __name__ == '__main__':
    init_display()
    display_text('1234')
  # Cleanup GPIO when done
#   GPIO.cleanup()