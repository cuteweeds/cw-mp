from machine import Pin, PWM
from utime import sleep_ms

r = PWM(Pin(11))
r.freq(1000)
r_value = 0
r_speed = 5

g = PWM(Pin(12))
g.freq(1000)
g_value = 0
g_speed = 5

b = PWM(Pin(13))
b.freq(1000)
b_value = 0
b_speed = 5

fps = 60
smooth = int(round(1000/fps,0))
max = 10000

while True:
    for rcycle in range(0,100/abs(r_speed)):
        r_value += round(r_speed*(rcycle*rcycle)/12350,4)
        if r_value < 0:
            r_value = 0
        r.duty_u16(int(r_value * max))
        sleep_ms(smooth)
        print(r_value,g_value,b_value)
    for gcycle in range(0,100/abs(g_speed)):
        g_value += round(g_speed*(gcycle*gcycle)/12350,4)
        if g_value < 0:
            g_value = 0
        g.duty_u16(int(g_value * max))
        sleep_ms(smooth)
        print(r_value,g_value,b_value)
    for bcycle in range(0,100/abs(b_speed)):
        b_value += round(b_speed*(bcycle*bcycle)/12350,4)
        if b_value < 0:
            b_value = 0
        b.duty_u16(int(b_value * max))
        sleep_ms(smooth)
        print(r_value,g_value,b_value)
    r_speed = -r_speed
    g_speed = -g_speed
    b_speed = -b_speed