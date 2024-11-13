from machine import Pin

#R, G, B channels are pins 11-13
r = Pin(10,Pin.OUT)
g = Pin(11,Pin.OUT)
b = Pin(12,Pin.OUT)
r.value(0),g.value(0),b.value(0)
smooth = 10
while True:
    r.value(1), g.value(0), b.value(0)
    machine.lightsleep(smooth)
    r.value(1), g.value(1), b.value(0)
    machine.lightsleep(smooth)
    r.value(0), g.value(1), b.value(1)
    machine.lightsleep(smooth)
    r.value(), g.value(1), b.value(1)
    machine.lightsleep(smooth)
    r.value(0), g.value(0), b.value(1)
    machine.lightsleep(smooth)
    r.value(1), g.value(0), b.value(1)
    machine.lightsleep(smooth)
    r.value(1), g.value(1), b.value(1)
    machine.lightsleep(smooth)
    r.value(1), g.value(0), b.value(1)
    machine.lightsleep(smooth)
    r.value(0), g.value(0), b.value(1)
    machine.lightsleep(smooth)
    r.value(0), g.value(1), b.value(1)
    machine.lightsleep(smooth)
    r.value(0), g.value(1), b.value(0)
    machine.lightsleep(smooth)
    r.value(1), g.value(1), b.value(0)
    machine.lightsleep(smooth)
    r.value(1), g.value(0), b.value(0)
    machine.lightsleep(smooth)

#    r.on()
#    machine.lightsleep(smooth)
#    g.on() #rg
#    machine.lightsleep(smooth)
#    r.off() #g
#    machine.lightsleep(smooth)
#    b.on() #gb
#    machine.lightsleep(smooth)
#    g.off() #b
#    machine.lightsleep(smooth)
#    r.on() 
#    g.on() #W
#    machine.lightsleep(smooth)
#    g.off() #br
#    machine.lightsleep(smooth)
#    g.on() #W
#    machine.lightsleep(smooth)
#    r.off
#    g.off() #b
#    machine.lightsleep(smooth)
#    g.on() #bg
#    machine.lightsleep(smooth)
#    b.off() #g
#    machine.lightsleep(smooth)
#    r.on() #rg
#    machine.lightsleep(smooth)
