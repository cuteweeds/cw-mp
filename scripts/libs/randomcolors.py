#import machine
import time, random
# Pin Assignments
# R LED - GP10 (14)
# G LED - GP11 (15)
# B LED - GP14 (19)
# SW1 - GP2 (4) & Gnd
# SW2 - GP15 (20) & 3.3V (36)

##red = Pin(10, Pin.OUT)
##green = Pin(11, Pin.OUT)
##blue = Pin(19, Pin.OUT)
#red, green, blue = Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(19, Pin.OUT)
#red.value(0)
#green.value(0)
#blue.value(0)

red, green, blue = random.random(), random.random(), random.random()
colors, maxwidth =(red, green, blue), 0

while True:
    signa = random.random()
    signb = random.random()
    signc = random.random()
    signweird = random.random()
    n = random.random()/2
    o = random.random()/2
    p = random.random()/2
    if signa > 0.49:
        n = -o
    if signb > 0.49:
        o = -p
    if signc > 0.49:
        p = -n
    if signweird > .95:
        blue+= 1-(n+o+p)/3
    if signweird < .05:
        blue -= 1-(n+o+p)/3
#        n= -1
#    else:
#        n=1
    #red.value(min(1,red+n))
    #green.value(min(1,green+n))
    #blue.value(min(1,blue+n))
    #machine.lightsleep_ms(80)
    colors=(red+n,green+o,blue+p)
    #red, green, blue = min(1,red+n), min(1,green+o), min(1,blue+p)
    #colors=(red, green, blue)
    spread = max(red,green, blue) - min(red,green,blue)
    if spread > maxwidth:
        maxwidth = spread
        #print("***************************************** "+str(maxwidth))
#    print(red,green,blue)
    print(colors)
    time.sleep(.1)