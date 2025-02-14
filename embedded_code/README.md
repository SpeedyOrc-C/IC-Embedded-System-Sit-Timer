
# Project File Structure

This project consists of several Python modules, each serving a distinct function. Below is a breakdown of the files and their responsibilities:

- **[display.py](display.py)**

  - Handles communication with the TM1637 4-digit 7-segment display.
  - Contains functions to initialize and send data to the display, including `init_display` and `display_text`.
- **[flex_sensor.py](flex_sensor.py)**

  - Manages interactions with the flex sensor through I2C/SPI using the `smbus2` interface.
  - Provides the function `read_flex_sensor` to read sensor values.
- **[http_api.py](http_api.py)**

  - Implements HTTP API functions to pair devices and post sensor data (both sit and stand events) to a remote server.
  - Contains functions such as `post_sit_data`, `post_stand_data`, `get_pairing_code`, and `is_paired`.
- **[offline_data.py](offline_data.py)**

  - Manages storing events locally when network connectivity is unavailable.
  - Includes logic to record events (`store_offline_data`) and process stored events (`process_offline_data`) when connectivity is restored.
- **[ultra_sensor.py](ultra_sensor.py)**

  - Interacts with an ultrasonic sensor to measure distance using the RPi.GPIO interface.
  - Contains the `get_distance` function for sensor measurement.
- **[main.py](main.py)**

  - Serves as the entry point of the application.
  - Coordinates sensor readings (from both the flex sensor and ultrasonic sensor), display updates, pairing, and HTTP API interactions.
  - Spawns a thread to update the display and checks sensor values to trigger sit or stand events.
