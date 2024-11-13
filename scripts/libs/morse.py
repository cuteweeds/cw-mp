from machine import Pin, Timer
led = Pin(25, Pin.OUT)
timer = Timer()

# Write your message in the quotes below, you whore.
psst = 'WHORE'

def short():
    led.value(1)
    machine.lightsleep(150)
    led.value(0)
    machine.lightsleep(100)

def long():
    led.value(1)
    machine.lightsleep(350)
    led.value(0)
    machine.lightsleep(100)

def morsulate(l):
    if l == 'a' or l =='A':
        short()
        long()
    elif l == 'b' or l =='B':
        long()
        short()
        short()
        short()
    elif l == 'c' or l =='C':
        long()
        short()
        long()
        short()
    elif l == 'd' or l =='D':
        long()
        short()
        short()
    elif l == 'e' or l =='E':
        short()
    elif l == 'f' or l =='F':
        short()
        short()
        long()
        short()
    elif l == 'g' or l =='G':
        long()
        long()
        short()
    elif l == 'h' or l =='H':
        short()
        short()
        short()
        short()
    elif l == 'i' or l =='I':
        short()
        short()
    elif l == 'j' or l =='J':
        short()
        long()
        long()
        long()
    elif l == 'k' or l =='K':
        long()
        short()
        long()
    elif l == 'l' or l =='L':
        short()
        long()
        short()
        short()
    elif l == 'm' or l =='M':
        long()
        long()
    elif l == 'n' or l =='N':
        long()
        short()
    elif l == 'o' or l == 'O':
        long()
        long()
        long()
    elif l == 'p' or l =='P':
        short()
        long()
        long()
        short()
    elif l == 'q' or l =='Q':
        long()
        long()
        short()
        long()
    elif l == 'r' or l =='R':
        short()
        long()
        short()
    elif l == 's' or l == 'S':
        short()
        short()
        short()
    elif l == 't' or l =='T':
        long()
    elif l == 'u':
        short()
        short()
        long()
    elif l == 'v' or l =='V':
        short()
        short()
        short()
        long()
    elif l == 'w' or l =='W':
        short()
        long()
        long()
    elif l == 'x' or l =='X':
        long()
        short()
        short()
        long()
    elif l == 'y' or l =='Y':
        long()
        short()
        long()
        long()
    elif l == 'z' or l =='Z':
        long()
        long()
        short()
        short()

while 1==1:
    for i in range(0,len(psst)):
        morsulate(psst[i])
    morsulate('')
    machine.lightsleep(1000)