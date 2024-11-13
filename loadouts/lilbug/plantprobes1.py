from machine import Pin, ADC
import time
import bme280
interval = 1000
timer = time.ticks_ms()

while True:
    if time.ticks_ms() - timer > interval:
        if bme280.reading(20000) == True:
            print('over threshold')
        
        timer = time.ticks_ms()