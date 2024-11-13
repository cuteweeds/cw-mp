from machine import Pin
from utime import sleep
test=1

class RGB:
    x=[0,0,0]
    r=[1,0,0]
    y=[1,1,0]
    g=[0,1,0]
    c=[0,1,1]
    b=[0,0,1]
    v=[1,0,1]
    w=[1,1,1]
    def __init__(self,r,g,b):
        self.rpin=Pin(r,Pin.OUT)
        self.gpin=Pin(g,Pin.OUT)
        self.bpin=Pin(b,Pin.OUT)
    def color(self,color):
        self.rpin.value(color[0])
        self.gpin.value(color[1])
        self.bpin.value(color[2])
class LED:
    def __init__(self,pin):
        self.state=Pin(pin,Pin.OUT)

if __name__=="__main__":
    if test==0:
        r=Pin(13,Pin.OUT)
        g=Pin(14,Pin.OUT)
        b=Pin(15,Pin.OUT)
        while True:
            r.toggle()
            sleep(1)
            g.toggle()
            sleep(1)
            b.toggle()
            sleep(1)
    if test==1:
        led=RGB(13,14,15)
        value=[0,0,1]
        led.color(led.x)
    if test==2:
        led=LED(12)
        led.state.off()

