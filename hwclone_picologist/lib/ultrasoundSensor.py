from machine import Pin
import utime

test_loop = 3
low_hold = 26 ; high_hold = 54
max_dist= 40 ; min_dist = 5
timepassed = 0 ; signaloff = 0 ; signalon = 0

class hcsr04:
        
        # Calibrated constants
        max_dist= 40
        min_dist = 5
        valrange = min_dist - max_dist
        
        def __init__(self, trigger, echo):
            self.trigger = Pin(trigger, Pin.OUT)
            self.echo = Pin(echo, Pin.IN)
            
        def reading(self):
            reading = ultra(self.trigger, self.echo)
            return reading
                

def compress(raw):         # report readings under low point as low, over high point as high
    if raw < min_dist: raw = min_dist;
    if raw > max_dist: raw = max_dist;
    return raw

def ultraa():
    trigger.low()
    utime.sleep_us(low_hold)
    trigger.high()
    utime.sleep_us(high_hold)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = compress((timepassed * 0.0343) / 2)
    return distance


def ultra(trigger, echo):
    global timepassed, signaloff, signalon
    trigger.low()
    utime.sleep_us(low_hold)
    trigger.high()
    utime.sleep_us(high_hold)
    trigger.low()
    if echo.value() == 0:
        signaloff = utime.ticks_us()
    if echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print(distance)
   
if __name__ == "__main__":
    echo = Pin(3, Pin.IN)
    trigger = Pin(2, Pin.OUT)

    if test_loop == 1:
        max_dist= 80 ; min_dist = 5 ; valrange = min_dist - max_dist
        probe = hcsr04(3,2)
        while True:
            print(ultra(probe.trigger,probe.echo))
            utime.sleep(0.1)
        
    if test_loop == 2:
        ultrasound = hcsr04(trigger,echo)
        while True:
            print(ultrasound.reading())
            print(timepassed)

    if test_loop == 3:
        while True:
            ultraa()
            utime.sleep(0.1)