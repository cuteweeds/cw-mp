"""
    Project Name: board.py
    File Name: board.py
    Author: GurgleApps.com
    Date: 2021-04-01
    Description: Detects the board type
"""
import sys
import os
from machine import Pin

class Board:
    class BoardType:
        PICO_W = 'Raspberry Pi Pico W'
        PICO = 'Raspberry Pi Pico'
        ESP8266 = 'ESP8266'
        ESP32 = 'ESP32'
        UNKNOWN = 'Unknown'

    def __init__(self):
        self.type = self.detect_board_type()

    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine = os.uname().machine.lower()

        if sysname == 'rp2' and 'pico w' in machine:
            return self.BoardType.PICO_W
        elif sysname == 'rp2' and 'pico' in machine:
            return self.BoardType.PICO
        elif sysname == 'esp8266':
            return self.BoardType.ESP8266
        # Add more conditions for other boards here
        else:
            return self.BoardType.UNKNOWN

def set_pins():
    global led, BOARD_TYPE
    BOARD_TYPE = Board().type
    
    if BOARD_TYPE == Board.BoardType.PICO_W:
        led = Pin("LED", Pin.OUT)
    elif BOARD_TYPE == Board.BoardType.PICO:
        led = Pin(25, Pin.OUT)
    elif BOARD_TYPE == Board.BoardType.ESP8266:
        led = Pin(2, Pin.OUT)
    else:
        led = Pin(2, Pin.OUT)
    return(led)
        
if __name__ == "__main__":
    set_pins()
    print(f"Running as main.\n Board type: {BOARD_TYPE}.\n led: {led}")
    led.toggle()
    
else:
    set_pins()
    print(f"Board type: {BOARD_TYPE}.\n led: {led}\n")
    led.toggle()
