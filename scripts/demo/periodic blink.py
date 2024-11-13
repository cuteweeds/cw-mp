from machine import Pin, Timer
led = machine.Pin("LED",Pin.OUT)
timer = machine.Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5,mode=Timer.PERIODIC, callback=blink)