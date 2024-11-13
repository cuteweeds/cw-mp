from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from random import random
from utime import sleep

test=2

class display:
    def __init__(self,bus,sda,scl,freq,w,h):
        self.i2c=I2C(bus,sda=Pin(sda),scl=Pin(scl),freq=freq)
        self.display=SSD1306_I2C(w,h,self.i2c)

def pick_a_number(max):
    return int(round(random()*max,0))

if test==1:
    i2c=I2C(0,sda=Pin(16),scl=Pin(17),freq=400000)
    oled=SSD1306_I2C(128,32,i2c)
    
    for i in range(128):
        oled.fill(0)
        oled.text("   Leila is Cool B)",-i,0)
        oled.show()

    w="...risky??"
    x="wow"
    y="cool"#pick_a_number(10)
    z="neat"#pick_a_number(100)
    zz="nice"#pick_a_number(3)
    acceleration=True
    smileys=[" :)"," ;)"," ;D",">:D",">;D",">:0"]
    while True:
        for speed in range(6):
            for i in range(8):
                oled.fill(0)
                oled.text(str(w),i*2,-8+i)
                oled.text(str(x),i*4,0+i)
                oled.text(str(y),i*6,8+i)
                oled.text(str(z),i*8,16+i)
                oled.text(str(zz),i*10,24+i)
                if acceleration==True:
                    oled.text(smileys[speed],104,0)
                    oled.show()
                    pause=.05-speed/100
                    sleep(pause)
                else:
                    oled.text(smileys[5-speed],104,0)
                    oled.show()
                    pause=speed/100
                    sleep(pause)

            for i in range(8):
                i=8-i
                oled.fill(0)
                oled.text(str(w),i*2,-8+i)
                oled.text(str(x),i*4,0+i)
                oled.text(str(y),i*6,8+i)
                oled.text(str(z),i*8,16+i)
                oled.text(str(zz),i*10,24+i)
                if acceleration==True:
                    oled.text(smileys[speed],104,0)
                    oled.show()
                    pause=.05-speed/100
                    sleep(pause)
                else:
                    oled.text(smileys[5-speed],104,0)
                    oled.show()
                    pause=speed/100
                    sleep(pause)
        acceleration=not acceleration

if test==2:
    oled=display(0,16,17,400000,128,32)
    oled.display.text("textual",3,6)
    oled.display.show()
