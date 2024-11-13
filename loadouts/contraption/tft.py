from machine import Pin, Timer,SPI
import time
class st7735:
    def __init__(self):        
        # configure pins for output
        self.reset=Pin(10,Pin.OUT)
        self.cs=Pin(9,Pin.OUT)
        self.a0=Pin(11,Pin.OUT)
        self.spi=SPI(0,baudrate=20000000,polarity=1,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(12),mosi=Pin(13))
        self.cs.value(1)
        self.reset.value(1)
        time.sleep_ms(10)
         
        self.reset.value(0)
        time.sleep_ms(200)
         
        self.reset.value(1)
        time.sleep_ms(200)
        self.cs.value(200)
        time.sleep_ms(200)
         
        self.cs.value(0)
        time.sleep_ms(20)
         
        self.command(1) # software reset
        time.sleep_ms(100)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0x11)
        time.sleep_ms(120)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)        
        time.sleep_ms(1)
         
        self.command(0xb1)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c);
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0xb2)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c);        
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0xb3)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0xb4)
        self.data(0x03)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0x36)
        self.data(0xc8)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0x3a)
        self.data(0x05)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0x29)
        time.sleep_ms(100)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
         
        self.command(0x2c)          
        self.fillRectangle(0,0,128,160,0)
         
    def command(self,cmd):
        self.a0.value(0)
        msg=bytearray()
        msg.append(cmd)
        self.spi.write(msg)
         
    def data(self,cmd):
        self.a0.value(1)
        msg=bytearray()
        msg.append(cmd)
        self.spi.write(msg)        
    def openAperture(self,x1,y1,x2,y2):
        self.command(0x2a)
        self.data(x1 >> 8)
        self.data(x1 & 0xff)
        self.data(x2 >> 8)
        self.data(x2 & 0xff)
        self.command(0x2b)
        self.data(y1 >> 8)
        self.data(y1 & 0xff)
        self.data(y2 >> 8)
        self.data(y2 & 0xff)        
        self.command(0x2c)
    def fillRectangle(self,x1,y1,w,h,colour):
        self.openAperture(x1,y1,x1+w-1,y1+h-1)        
        pixelcount=h*w        
        self.command(0x2c)
        self.a0.value(1)
        msg=bytearray()
        while(pixelcount >0):
            pixelcount = pixelcount-1          
            msg.append(colour >> 8)
            msg.append(colour & 0xff)
        self.spi.write(msg)
    def putPixel(self,x,y,colour):
        self.openAperture(x,y,x+1,y+1)        
        self.a0.value(1)
        msg=bytearray()
        msg.append(colour >> 8)
        msg.append(colour & 0xff)
        self.spi.write(msg)
    def drawLine(self,x0,y0,x1,y1,colour):
        if ( (abs(y1-y0) < abs(x1-x0))):
             if (x0 > x1):
                 self.drawLineLowSlope(x1,y1,x0,y0,colour)
             else:
                 self.drawLineLowSlope(x0,y0,x1,y1,colour)
        else:
            if (y0 > y1):
                self.drawLineHighSlope(x1,y1,x0,y0,colour)
            else:
                self.drawLineHighSlope(x0,y0,x1,y1,colour)
             
    def drawLineLowSlope(self,x0,y0,x1,y1,colour):
        # Reference : https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm    
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if (dy < 0):
            yi = -1
            dy = -dy
        D = 2*dy - dx
        y = y0
        for x in range(x0,x1+1):
            self.putPixel(x,y,colour)
            if (D > 0):
                y = y + yi
                D = D - 2*dx
            D=D + 2*dy
    def drawLineHighSlope(self,x0,y0,x1,y1,colour):
        # Reference : https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm    
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if (dx < 0):
            xi = -1
            dx = -dx
        D = 2*dx - dy
        x = x0
        for y in range(y0,y1+1):
            self.putPixel(x,y,colour)
            if (D > 0):
                x = x + xi
                D = D - 2*dy
            D=D + 2*dx