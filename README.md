# ELEC60013 Embedded Systems: Coursework 1
## SitSense Project Overview

[SitSense](https://while-you-seat.speedyorc-chen.site) is an innovative smart monitoring system designed to track your sitting habits and help prevent health issues caused by prolonged sitting. This system uses a Raspberry Pi, a GPIO ultrasonic sensor, and an I2C flex sensor to detect when someone is seated and for how long.

## conponents

This repository contains three main components:

### **Website**  

The [website](website) is built using [SvelteKit](https://kit.svelte.dev/) and [TypeScript](https://www.typescriptlang.org/). It provides the user interface and API endpoints, for example:  

- User authentication via log-in and log-out endpoints.
- Device management including pairing and deletion with API routes under [src/routes/dashboard](website/src/routes/dashboard).

### **Database**

The [database](database) folder contains SQL scripts for managing data storage. It defines the schema and operations for:

- Storing device information and pairing logs.
- Handling user sessions and interactions.

### **Embedded Code**  

The [embedded_code](embedded_code) directory holds Python scripts that run on embedded devices. Key scripts include:

- [display.py](embedded_code/display.py) – manages display functions.
- [flex_sensor.py](embedded_code/flex_sensor.py) and [ultra_sensor.py](embedded_code/ultra_sensor.py) – handle sensor data.
- [http_api.py](embedded_code/http_api.py) – facilitates communication with the website API.
- [main.py](embedded_code/main.py) – the entry point for device operations.
