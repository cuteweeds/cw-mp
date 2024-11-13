print("Loading cfg … ", end = "")

### ENABLE BLINK CODES FOR TROUBLESHOOTING (REQUIRES BOARD LED)
from board.blinker import blinker

### USER SETTINGS
## Devices
ST7735_ON       = True        # ENABLE ST7735 (128x160 LCD)
## Time
TZ              = -5          # Set time zone
## Visuals
lines           = 8           # Vertical steps per cycle
fade_cap        = 2           # Iterations of fadeout (higher = slower refresh rate)
fontsize        = 2           # 1-3 for best results on ST7735 (2 is good)
padding         = 3           # To center text
base_brightness = 1           # 1 = normal, 2 = dim, etc.
highlight       = "on"        # "on": color bar in bg ; "off": none
notxt           = False       # False = render time ; True = keep display blank (for testing)
h_off           = False       # Text doesn't move horizontally
## Debug modes
debug           = "off"       # "color", "position", or "off"

### DETECT BOARD AND DEVICE SUPPORT IF KNOWN
from board.board import Board
BOARD_TYPE = Board().type
print("found", BOARD_TYPE)
if BOARD_TYPE == Board.BoardType.PICO_W:
    BOARD_LED_ON=True
    BOARD_LED_PIN = "LED"
    BLUETOOTH_ON=True
    WIFI_ON=True
    SPI1_CIPO   = None
    SPI1_SCK    = 10
    SPI1_COPI   = 11
    SPI1_A0     = 8
    SPI1_RESET  = 12
    SPI1_CS     = 9
    SPI0_CIPO   = None
    SPI0_CSN    = None
    SPI0_SCK    = None
    SPI0_COPI   = None
    SPI0_CE     = None    
    BLINK = blinker(BOARD_LED_PIN)    
    BLINK.pattern(2,.05,.15)
elif BOARD_TYPE == Board.BoardType.PICO:
    BOARD_LED_ON=True
    BOARD_LED_PIN = 25
    BLUETOOTH_ON = False
    WIFI_ON = True
    SPI1_CIPO   = None
    SPI1_SCK    = 10
    SPI1_COPI   = 11
    SPI1_A0     = 12
    SPI1_RESET  = 13
    SPI1_CS     = 14
    SPI0_CIPO   = 16
    SPI0_CSN    = 17
    SPI0_SCK    = 18
    SPI0_COPI   = 19
    SPI0_CE     = 20
    BLINK = blinker(BOARD_LED_PIN)     
    BLINK.pattern(2,.25,.05)
elif BOARD_TYPE == Board.BoardType.ESP8266:
    BOARD_LED_ON = False
    BOARD_LED_PIN = 2
    WIFI_ON = True
    BLUETOOTH_ON = False
else:
    BOARD_TYPE = "unknown board"
    BLUETOOTH_ON = False
    WIFI_ON = False
    BOARD_LED_ON = False
    print("Unknown board detected.")

### SETUP DEVICE PINS
if ST7735_ON == True:
    try:
        tft_SCK = SPI1_SCK
        tft_SDA = SPI1_COPI
        tft_A0_ = SPI1_A0
        tft_RES = SPI1_RESET
        tft_CS_ = SPI1_CS
        tft_BL = 13
    except:
        raise Exception("Set SPI pins in cfg to attach devices")