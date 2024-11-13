from machine import ADC, Pin
import time

interval = 1000

def reading (threshold):
    reading = adc.read_uint16()
    time.sleep_ms(interval)
    reading = adc.read_uint16()
    print(reading)
    if reading > threshold:
        return True