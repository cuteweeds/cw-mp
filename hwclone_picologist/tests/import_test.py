from machine import Pin
import utime
from lib.moistureSensor import Probe as probe

# init Objects
dipper = probe("Rutger",26)

# sensor check periods
dipperPeriod = 100

# Poll loop
while True:
    bounce = utime.ticks_ms()
    if bounce > dipperPeriod:
        bounce = 0
        wetness = dipper.wetness()
    
    print(f"The view from {__name__} is {wetness:2}%")