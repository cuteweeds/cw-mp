from utime import sleep_ms
from hw_toggleLed import toggle
from hw_statusPy import status

from board.board import boardID

Board = boardID()
print("Detected " + Board.type)
print(Board.Pins["LED"])


count=0

while True:
    if count % 8 == 0:
        toggle()
    if count % 10 == 0:
        status('xx')
    sleep_ms(100)
    count+=1