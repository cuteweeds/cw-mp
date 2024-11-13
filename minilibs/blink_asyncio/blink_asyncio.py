## asyncio library to control LEDS.
## blinker objects use method pattern(blinks,ont,offt) to trigger sequences of blinks, intended as a visual indicator.
## currently fails to import asyncio on rpi pico, todo: try newer firmware

from machine import Pin
from utime import sleep
import asyncio

class blinker:
    def __init__(self,pin):
        self.pin = Pin(pin,Pin.OUT)
        
    async def pattern(self,blinks,ont,offt):
        count=0
        while count < blinks:
            count += 1
            self.pin.on()
            await asyncio.sleep(ont)
            self.pin.off()
            await asyncio.sleep(offt)

class disable:
    def __init__(self,pin):
        self.pin = Pin(pin,Pin.OUT)
        
    def pattern(self,blinks,ont,offt):
        pass

if __name__ =="__main__":
    light1 = blinker(12)
    light2 = blinker(14)
    light1.pattern(15,.1,.5)
    light2.pattern(15,.2,.2)