from utime import sleep
from random import random
from machine import Pin,PWM
light="on"
red, green, blue = random(), random(), random()
colors, maxwidth =(red, green, blue), 0
RPin=Pin(13,Pin.OUT)
GPin=Pin(14,Pin.OUT)
BPin=Pin(15,Pin.OUT)
R=PWM(RPin,freq=1000,duty_u16=0) #; R.freq(1000) #; R.init(duty_u16=0)
G=PWM(GPin,freq=1000,duty_u16=0) #; G.freq(1000) #; G.init(duty_u16=0)
B=PWM(BPin,freq=1000,duty_u16=0) #; B.freq(1000) #; B.init(duty_u16=0)

if __name__=="__main__":
    while True:
        signa = random()
        signb = random()
        signc = random()
        signweird = random()
        n = random()/2
        o = random()/2
        p = random()/2
        if signa > 0.49:
            n = -o
        if signb > 0.49:
            o = -p
        if signc > 0.49:
            p = -n
        if signweird > .95:
            blue+= .39-(n+o+p)/3
        if signweird < .05:
            blue -= .59-(n+o+p)/3
        colors=(red+n,green+o,blue+p)
        spread = max(red,green, blue) - min(red,green,blue)
        if spread > maxwidth:
            maxwidth = spread
#        print(colors)
        if light=="on":
            R.duty_u16(int(min(7000*(1%abs(colors[0])),65355))) # raise trailing decimals by 10^5, max 65535
            G.duty_u16(int(min(7000*(1%abs(colors[1])),65355)))
            B.duty_u16(int(min(7000*(1%abs(colors[2])),65355)))
        else:
            R.value(0)
            G.value(0)
            B.value(0)
        sleep(.05)