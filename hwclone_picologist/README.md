## This version downloaded from MCU in January 2024. Working Great.
## BT and Wifi, date checking, Temp, Pressure, and Water Sensors displaying and logging.

# Picology
A homebrew, easy-to-use and versatile plant-care system. 

## Goals:
1. Easy to set up and reconfigure
2. Compatible with RPi Pico and ESP23 controllers
3. Supports inexpensive, reliable sensors and mechanical devices
4. Wifi & Bluetooth support
5. Data logging locally and online
6. Plays nice with prototyping frameworks

## For Pi Pico & Pico W
RPI Pico and Pico W are both supported.

## For ESP32
### Supported controllers
The following controllers are targetted for support
- ESP32-S3
- ESP32-C3

## Supported Peripherals
### Sensors
Code supports any number of each type of sensors. Each sensor has a flexible wrapper so it can be invoked as an object of class **"probe"** and passed all necessary parameters. Sensors are polled at a frequency that can be set universally or independently.
- Capacitative soil moisture sensors
- BMP280 Temp/Barometric pressure
- Ultrasonic rangefinder (no use case yet) 
- **Todo:** BME280 Temp/Humidity
- **Todo:** RoHS-compliant phototransistor
- **Todo:** Photoresistor
- **Todo:** DS18B20 High-Precision 1-Wire Thermometer
- **Todo:** Air quality / PM2.5 sensor

### Feedback/Control
- **Todo:** Water pump (3.3V–5V)
- **Todo:** Dimmer / Relay
- **Todo:** Shift Register
