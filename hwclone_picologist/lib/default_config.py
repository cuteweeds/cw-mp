LOG_LINELENGTH_MAX = 100 # Max characters per line
LOG_FILESIZE_MAX = LOG_LINELENGTH_MAX * 8 * 200 # reserves up to 100 chars per line

# CONFIGURE SENSORS AND DISPLAYS
print("Loading device configurations")
BMP280_S1_ON = True            # *** BMP280 Thermometer/Barometer
LDR_ON = True                  # Light-Dependent Resistor
MOISTURE_S1_ON =True           # *** Capacitative Moisture Sensor 1
MOISTURE_S2_ON = True          # *** Capacitative Moisture Sensor 2
OLED91_ON = True               # 0.91" OLED config
ULTRASOUND_S1_ON = False       # *** HCSR-04 Ultrasonic Rangefinder

# DEFAULT VALUES
POLL_INTERVAL = 1000           # Frequency in ms to poll and report data
RGB_WARN_PIN1 = 13             # Sensor warning threshold indicator lights
RGB_WARN_PIN2 = 14
RGB_WARN_PIN3 = 15
LED_WARN1_PIN = 12
BOARD_LED_STATE = 0            # Misc. parameters here
TZ = -4                        # Fuck it we're doing EST/EDT

# WIFI
SSID = "MrHouse2.4"            # "BELL875"           # "MrHouse2.4"
PASSWORD = "surf ninjas"       # "EF31A1FD6F64"      # "surf ninjas"