from machine import Pin
import utime
echo = Pin(0, Pin.IN)
trigger = Pin(1, Pin.OUT)
def ultra():
   trigger.low()
   utime.sleep_us(10)
   trigger.high()
   utime.sleep_us(25)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print(distance)
while True:
   ultra()
   utime.sleep(1)
