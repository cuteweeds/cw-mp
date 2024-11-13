from utime import sleep
from random import random
from machine import Pin,PWM

TEST=3
LIGHT="on"
RPin=13
GPin=14
BPin=15

R=PWM(Pin(RPin,Pin.OUT),freq=1000,duty_u16=0) 
G=PWM(Pin(GPin,Pin.OUT),freq=1000,duty_u16=0) 
B=PWM(Pin(BPin,Pin.OUT),freq=1000,duty_u16=0) 
RED, GREEN, BLUE = random(), random(), random()
COLORS, MAXWIDTH =(RED, GREEN, BLUE), 0

class RGB:
    def __init__(self,R,G,B):
        self.R=PWM(Pin(R,Pin.OUT),freq=1000,duty_u16=0)
        self.G=PWM(Pin(G,Pin.OUT),freq=1000,duty_u16=0)
        self.B=PWM(Pin(B,Pin.OUT),freq=1000,duty_u16=0)
        
    def color(self,colors):
        FACTOR=7000
        MAX=65355
        
        # Multiplies color value by FACTOR to obtain 16-bit duty cycle (max 65535)         
        try:
            self.R.duty_u16(int(min(FACTOR*(1%abs(colors[0])),MAX)))
        except:
            self.R.duty_u16(0)
        try:
            self.G.duty_u16(int(min(FACTOR*(1%abs(colors[1])),MAX)))
        except:
            self.G.duty_u16(0)
        try:
            self.B.duty_u16(int(min(FACTOR*(1%abs(colors[2])),MAX)))
        except:
            self.B.duty_u16(0)

    def anycolor(self):
        global COLORS, RED, GREEN, BLUE

        signr = random() ; n = random()/2
        signg = random() ; o = random()/2
        signb = random() ; p = random()/2
        if signr > .49:
            RED+=n
        else:
            RED-=n
        if signg > .49:
            GREEN+=o
        else:
            GREEN-=o
        if signb > .49:
            BLUE+=p
        else:
            BLUE-=p
        COLORS=(RED,GREEN,BLUE)
        self.color(COLORS)
        
    def breathe(self,rmax,gmax,bmax):
        global COLORS, RED, GREEN, BLUE
        time=10
        pause=.05
        r_delta=int(rmax/time)
        g_delta=int(gmax/time)
        b_delta=int(bmax/time)
        period=int(65355/max(r_delta,g_delta,b_delta))
        for i in range(period):
            RED=int(RED+r_delta)
            GREEN=int(GREEN+g_delta)
            BLUE=int(BLUE+b_delta)
            COLORS = (RED,GREEN,BLUE)
            print(COLORS)
            self.R.duty_u16(RED)
            self.G.duty_u16(GREEN)
            self.B.duty_u16(BLUE)
            sleep(pause)
        for i in range(period):
            RED=int(RED-r_delta)
            GREEN=int(GREEN-g_delta)
            BLUE=int(BLUE-b_delta)
            COLORS = (RED,GREEN,BLUE)
            self.R.duty_u16(RED)
            self.G.duty_u16(GREEN)
            self.B.duty_u16(BLUE)
            print(COLORS)
            sleep(pause)
            

if __name__=="__main__":
    if TEST==1:
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
                BLUE+= .39-(n+o+p)/3
            if signweird < .05:
                BLUE -= .59-(n+o+p)/3
            COLORS=(RED+n,GREEN+o,BLUE+p)
            spread = max(RED,GREEN, BLUE) - min(RED,GREEN,BLUE)
            if spread > MAXWIDTH:
                MAXWIDTH = spread
    #        print(COLORS)
            if LIGHT=="on":
                R.duty_u16(int(min(7000*(1%abs(COLORS[0])),65355))) # raise trailing decimals by 10^5, max 65535
                G.duty_u16(int(min(7000*(1%abs(COLORS[1])),65355)))
                B.duty_u16(int(min(7000*(1%abs(COLORS[2])),65355)))
            else:
                R.value(0)
                G.value(0)
                B.value(0)
            sleep(.05)
    if TEST==2:
        if LIGHT=="on":
            rgb=RGB(13,14,15)
            rgb.anycolor()
    if TEST==3:
        if LIGHT=="on":
            rgb=RGB(13,14,15)
            COLORS=(0,0,0)
            rgb.color(COLORS)
            rgb.anycolor()
            rmax=int(min(RED+random()*20355,40000-random()*20000))
            gmax=int(min(GREEN+random()*20355,40000-random()*20000))
            bmax=int(min(BLUE+random()*20355,40000-random()*20000))
            rgb.breathe(rmax,gmax,bmax)  # grade colors from 0 to max (3 pairs of random max values)
            