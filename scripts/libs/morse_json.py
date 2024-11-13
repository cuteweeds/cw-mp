psst = 'Hi, slut!' # Write your message in the quotes, you whore.

from machine import Pin
import json, time, sys

sm_led, R_led = Pin(25, Pin.OUT), Pin(28,Pin.OUT) # Set pins and timings
rbutton = Pin(2, Pin.IN, Pin.PULL_UP) 
interrupt, debounce = 0, 0
dot = 50
dash = 3 * dot

def Press(rbutton):
    global interrupt, debounce
    if (time.ticks_ms() - debounce) > 200:
        interrupt = 1
        debounce = time.ticks_ms()
rbutton.irq(trigger=Pin.IRQ_FALLING,handler=Press)

def prepdict(lst): #parse list of key-values to dictionary
    rdict = {}
    for i in range(len(lst)):
        rdict[lst[i]["key"]] = lst[i]["val"]
    return rdict

def sendatelegraph(string): #translate character codes to morse bits and take to the airwaves
    global interrupt, debounce
    for char in string:
        if interrupt == 1:
            sys.exit()
        code = dict.get(char)
        transmit(code)
        hold(dash)

def transmit(code): #transmit bits to pin outs
    for bit in code:
        if bit == "0":
            sm(), hold(dot)
        elif bit == "1":
            lm(), hold(dot)
        elif bit == "2":
            hold(dot)

def sm():         #dot
    sm_led.on(), R_led.on()
    hold(dot)
    sm_led.off(), R_led.off()

def lm():         #dash
    sm_led.on(), R_led.on()
    hold(dash)
    sm_led.off(), R_led.off()

def hold(interval):  #pause
    machine.lightsleep(interval)

with open("morse.json", "r") as data:   #load code definition
    raw = json.load(data)
dict = prepdict(raw)

while True:
    sendatelegraph(psst)