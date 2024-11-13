from machine import Pin
import time

gled = Pin(28, Pin.OUT)
rled = Pin(14, Pin.OUT)
rbutton = Pin(2, Pin.IN, Pin.PULL_UP)
lbutton = Pin(15, Pin.IN, Pin.PULL_DOWN)

rled.value(1), gled.value(1)
rcount, lcount = 0, 0
ri_flag = 0
li_flag = 0
debounce = 0

def Rpress(rbutton):
    global ri_flag, debounce
    if (time.ticks_ms() - debounce) > 250:
        ri_flag = 1
        debounce = time.ticks_ms()
    
def Lpress(lbutton):
    global li_flag, debounce
    if (time.ticks_ms() - debounce) > 250:
        li_flag = 1
        debounce = time.ticks_ms()

rbutton.irq(trigger=Pin.IRQ_FALLING,handler=Rpress)
lbutton.irq(trigger=Pin.IRQ_RISING,handler=Lpress)

while True:
    if ri_flag == 1:
        rcount += 1
        print("R button pushed {} times".format(rcount))
        rled.toggle()
        ri_flag = 0

    if li_flag == 1:
        lcount += 1
        print("L button pushed {} times".format(lcount))
        gled.toggle()
        li_flag = 0