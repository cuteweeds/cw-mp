import time
from machine import Pin
from board import Board

BOARD_TYPE = Board().type
print("Board type: " + BOARD_TYPE)

if BOARD_TYPE == Board.BoardType.PICO_W:
    led = Pin("LED", Pin.OUT)
elif BOARD_TYPE == Board.BoardType.PICO:
    led = Pin(25, Pin.OUT)
elif BOARD_TYPE == Board.BoardType.ESP8266:
    led = Pin(2, Pin.OUT)
else:
    led = Pin(2, Pin.OUT)
    
while True:
    led.on()
    time.sleep(.5)
    led.off()
    time.sleep(5)