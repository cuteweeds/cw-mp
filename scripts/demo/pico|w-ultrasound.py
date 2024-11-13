from machine import Pin
import utime
trigger = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

def ultra():
    trigger.low()
    utime.sleep_us(20)
    trigger.high()
    utime.sleep_us(50)
    trigger.low()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print(distance)
while True:
    print('running…')
    ultra()
    utime.sleep(1)