from machine import Pin

#Pin25 (orange jumper)
pin = Pin(28, Pin.OUT)
pin.value(0)
machine.lightsleep(100)

#onboard led
pin = Pin(25, Pin.OUT)
pin.value(0)
machine.lightsleep(100)

pin = Pin(5, Pin.OUT)
pin.value(0)

pin = Pin(2, Pin.OUT)
pin.value(0)

pin = Pin(15, Pin.OUT)
pin.value(0)

pin = Pin(14, Pin.OUT)
pin.value(0)

pin = Pin(10, Pin.OUT)
pin.value(0)

pin = Pin(11, Pin.OUT)
pin.value(0)

pin = Pin(12, Pin.OUT)
pin.value(0)

pin = Pin(13, Pin.OUT)
pin.value(0)