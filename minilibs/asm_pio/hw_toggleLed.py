from machine import Pin

def toggle():
    led = Pin("LED", Pin.OUT)
    led.toggle()