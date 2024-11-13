from machine import Pin
from utime import sleep

class blinker:
    def __init__(self,pin):
        self.pin = Pin(pin,Pin.OUT)
        
    def pattern(self,blinks,ont,offt):
        count=0
        while count < blinks:
            count += 1
            self.pin.on()
            sleep(ont)
            self.pin.off()
            sleep(offt)

class disable:
    def __init__(self,pin):
        self.pin = Pin(pin,Pin.OUT)
        
    def pattern(self,blinks,ont,offt):
        pass

if __name__ =="__main__":
    light = blinker(25)
    light.pattern(15,.1,.05)