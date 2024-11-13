import sys
import os

class Board:
    class BoardType:
        """Returns BoardType.Type as string."""
        PICO_W = 'RPi Pico W'
        PICO = 'RPi Pico'
        ESP8266 = 'ESP8266'
        ESP32 = 'ESP32'
        UNKNOWN = 'Unknown'
        """Add more boards here and in detect_board_type"""

    def __init__(self):
        self.type = self.detect_board_type()

    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine = os.uname().machine.lower()

        if sysname == 'rp2' and 'pico with' in machine:
            return self.BoardType.PICO
        elif sysname == 'rp2' and 'pico w ' in machine:
            return self.BoardType.PICO_W
        elif sysname == 'esp8266':
            return self.BoardType.ESP8266
        # Add more conditions for other boards here
        else:
            return self.BoardType.UNKNOWN

if __name__=="__main__":
    BOARD_TYPE = Board().type
    print("Detected " + BOARD_TYPE)