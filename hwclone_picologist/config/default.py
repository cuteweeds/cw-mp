# LOGGING SETTINGS
LOG_LINELENGTH_MAX = 100                        # Max characters per line
LOG_FILESIZE_MAX = LOG_LINELENGTH_MAX * 8 * 200 # reserves up to 100 chars per line

# CONFIGURE SENSORS AND DISPLAYS
print("Loading device configurations…", end = "")
BMP280_S1_ON = True            # *** BMP280 Thermometer/Barometer
LDR_ON = True                  # Light-Dependent Resistor
MOISTURE_S1_ON =True           # *** Capacitative Moisture Sensor 1
MOISTURE_S2_ON = True          # *** Capacitative Moisture Sensor 2
OLED91_ON = True               # 0.91" OLED config
ULTRASOUND_S1_ON = False       # *** HCSR-04 Ultrasonic Rangefinder
print("done.")

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

# GPIO DEVICES                 # Todo: SSID detection,g214 auto-connect known networks
if MOISTURE_S1_ON == True:
    MOISTURE_S1_PIN = 27                # Must be ADC Pin
    MOISTURE_S1_LOW = -3   #20         # Threshold to trigger dry response
    MOISTURE_S1_HIGH = 995 #75         # Threshold to trigger wet response                                         # -todo: append to list "sensor array"
if MOISTURE_S2_ON == True:               # …(type, name, pin, auto-serial)
    MOISTURE_S2_PIN = 26             
    MOISTURE_S2_LOW = None           
    MOISTURE_S2_HIGH = None          
if ULTRASOUND_S1_ON == True:
    ULTRASOUND_S1_TRIGGER = None     # Any GPIO
    ULTRASOUND_S1_ECHO = None        # Any GPIO  
if LDR_ON == True:
    LDR_PIN = 28
    LDR_LOW = -10         #25         # Thresholds to trigger lo/hi-light response
    LDR_HIGH = 770      #60          
     
# I2C DEVICES
if BMP280_S1_ON == True:
    BMP280_S1_BUS = 1                # Must be different bus than OLED (?)
    BMP280_S1_SCL = 19               # Must be I2C
    BMP280_S1_SDA = 18               # Must be I2C
    BMP280_S1_FREQ = 200000
if OLED91_ON == True:
    OLED_BUS = 0                     # Must be different bus than BME (?)
    OLED_SCL = 17                    # Must be I2C
    OLED_SDA = 16                    # Must be I2C
    OLED_FREQ = 400000
    OLED_WIDTH = 128                 # Redundant to include these in config if this is specifically for a 0.91" OLED
    OLED_HEIGHT = 32                 # ...

# DETECT BOARD AND WIRELESS SUPPORT IF KNOWN
print(__name__)
from board import Board
try:
    BOARD_TYPE = Board().type
    print("Board is: " + BOARD_TYPE)
    if BOARD_TYPE == Board.BoardType.PICO_W:
        BOARD_LED_ON=True
        BOARD_LED_PIN = "LED"
        BLUETOOTH_ON=True
        WIFI_ON=True
        from blinker import blinker
        BLINK = blinker(BOARD_LED_PIN)    
        BLINK.pattern(1,.25,0)
    elif BOARD_TYPE == Board.BoardType.PICO:
        BOARD_LED_ON=True
        BOARD_LED_PIN = 25
        BLUETOOTH_ON = False
        WIFI_ON = False
        from blinker import blinker
        BLINK = blinker(BOARD_LED_PIN)     
        BLINK.pattern(1,.25,0)
    elif BOARD_TYPE == Board.BoardType.ESP8266:
        BOARD_LED_ON = False
        BOARD_LED_PIN = 2
        WIFI_ON = True
        BLUETOOTH_ON = False
        from blinker import disable as blinker
        BLINK = blinker(BOARD_LED_PIN)    
        BLINK.pattern(1,.25,0)
    else:
        BOARD_TYPE = "unknown board"
        BLUETOOTH_ON = False
        WIFI_ON = False
        BOARD_LED_ON = False
        from blinker import disable as blinker
        BLINK.pattern(5,.25,.25)
        sleep(.5)
        BLINK.pattern(5,.25,.25)
except:
    BOARD_TYPE = "unknown board"
    BLUETOOTH_ON = False
    WIFI_ON = False
    BOARD_LED_ON = False  
  
  
# TODO: CONFIG CHECKING
    # TODO: If OLED_BUS = BMP280_BUS and both are ON=True, throw an error
    # TODO: Verify OLED W/H dimensions make sense
    # TODO: Try each initialized sensor to confirm connection