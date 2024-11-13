from machine import Pin
import time
button = Pin(2, Pin.IN, Pin.PULL_UP)
flag, debounce = 0, 0

def press(button):
    global flag, debounce
    if (time.ticks_ms() - debounce) > 250:
        flag = 1
        debounce = time.ticks_ms()
        return flag, debounce

button.irq(trigger=Pin.IRQ_FALLING,handler=press)

while True:
    if flag == 1:
        print(';st op')
        flag = 0