from machine import Pin, Timer,SPI
import urandom
import time
import st7735 
display=st7735.st7735()
 
while(1):
    x1=urandom.randint(0,120)
    y1=urandom.randint(0,150)
    x2=urandom.randint(0,120)
    y2=urandom.randint(0,150)
    w=urandom.randint(1,127-x1)
    h=urandom.randint(1,159-y1)
    colour=urandom.randint(0,65535)    
    display.drawLine(x1,y1,x2,y2,colour)