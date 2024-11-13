from machine import Pin, Timer
sm_led = Pin(25, Pin.OUT)
R_led = Pin(28,Pin.OUT)
timer = Timer()

# Write your message in the quotes below, you whore.
psst = 'WHORE'

def sm():
    sm_led.value(1)
    R_led.value(1)
    machine.lightsleep(150)
    sm_led.value(0)
    R_led.value(0)
    machine.lightsleep(100)

def lm():
    sm_led.value(1)
    R_led.value(1)
    machine.lightsleep(350)
    sm_led.value(0)
    R_led.value(0)
    machine.lightsleep(100)

def morsulate(l):
    if l == 'a' or l =='A':
        sm()
        lm()
    elif l == 'b' or l =='B':
        lm()
        sm()
        sm()
        sm()
    elif l == 'c' or l =='C':
        lm()
        sm()
        lm()
        sm()
    elif l == 'd' or l =='D':
        lm()
        sm()
        sm()
    elif l == 'e' or l =='E':
        sm()
    elif l == 'f' or l =='F':
        sm()
        sm()
        lm()
        sm()
    elif l == 'g' or l =='G':
        lm()
        lm()
        sm()
    elif l == 'h' or l =='H':
        sm()
        sm()
        sm()
        sm()
    elif l == 'i' or l =='I':
        sm()
        sm()
    elif l == 'j' or l =='J':
        sm()
        lm()
        lm()
        lm()
    elif l == 'k' or l =='K':
        lm()
        sm()
        lm()
    elif l == 'l' or l =='L':
        sm()
        lm()
        sm()
        sm()
    elif l == 'm' or l =='M':
        lm()
        lm()
    elif l == 'n' or l =='N':
        lm()
        sm()
    elif l == 'o' or l == 'O':
        lm()
        lm()
        lm()
    elif l == 'p' or l =='P':
        sm()
        lm()
        lm()
        sm()
    elif l == 'q' or l =='Q':
        lm()
        lm()
        sm()
        lm()
    elif l == 'r' or l =='R':
        sm()
        lm()
        sm()
    elif l == 's' or l == 'S':
        sm()
        sm()
        sm()
    elif l == 't' or l =='T':
        lm()
    elif l == 'u':
        sm()
        sm()
        lm()
    elif l == 'v' or l =='V':
        sm()
        sm()
        sm()
        lm()
    elif l == 'w' or l =='W':
        sm()
        lm()
        lm()
    elif l == 'x' or l =='X':
        lm()
        sm()
        sm()
        lm()
    elif l == 'y' or l =='Y':
        lm()
        sm()
        lm()
        lm()
    elif l == 'z' or l =='Z':
        lm()
        lm()
        sm()
        sm()

while 1==1:
    for i in range(0,len(psst)):
        morsulate(psst[i])
    morsulate('')
    machine.lightsleep(1000)