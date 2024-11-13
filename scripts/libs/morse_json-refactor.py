PSST = 'Hi, slut!'              """Write your message in the quotes, you whore."""

import json, time, sys
try:                                            """HARDWARE CONFIG"""
    from machine import Pin                     
    SM_LED = Pin(25, Pin.OUT)
    R_LED = Pin(28,Pin.OUT) 
    RBUTTON = Pin(2, Pin.IN, Pin.PULL_UP)
    RBUTTON.irq(trigger=Pin.IRQ_FALLING,handler=Press)
except Exception as e:
    print(e)

INTERRUPT = 0                                   """CONTROL VARIABLES"""
DEBOUNCE = 0
DOT = 50                                        """STANDARD MORSE DASH = 3 * DOT"""

def prepdict(lst):                              """LOADS ENCODINGS FROM JSON"""
    rdict = {}
    for i in range(len(lst)):
        rdict[lst[i]['key']] = lst[i]['val']
    return rdict

def sendatelegraph(string):                     """CONTROLS ENCODE & TRANSMIT"""
    global INTERRUPT, DOT, DICT
    for char in string:
        if INTERRUPT == 1:                      """ON INTERRUPT, EXITS IMMEDIATELY"""
            sys.exit()
        code = DICT.get(char.lower())
        transmit(code)
        hold(3 * DOT,'\n')                      """BTWN WORDS PAUSE (DOT) & NEWLINE"""

    def transmit(code):
        for bit in code:
            if bit <= 1:
                leds(DOT + bit * 2 * DOT)       """BIT = 0/1 HANDLED IN leds()"""
            else:
                hold(DOT,'')                    """BIT = 2/INVALID JUST PAUSE"""
            hold(DOT,'')                        """DOT-LENGTH SPACE BTWN BITS"""

    def leds(duration): 
        print(duration/DOT * '-', end='')
        try:
            SM_LED.value(duration/duration)
            R_LED.value(duration/duration)
            hold(duration,'')
            SM_LED.value(0)
            R_LED.value(0)
        except:
            hold(duration,'')

    def hold(duration,eol_char):
        for x in range(duration/dot):
            time.sleep(duration)
            print(" ",end=eol_char)

def Press(RBUTTON):                             """STOP ON BUTTON PRESS"""
    global INTERRUPT, DEBOUNCE
    if (time.ticks_ms() - DEBOUNCE) > 200:
        INTERRUPT = 1
        DEBOUNCE = time.ticks_ms()

try:
    with open('morse-refactor.json', 'r') as data:
        raw = json.load(data)
    DICT = prepdict(raw)
except Exception as e:
    print(e)
    sys.exit()                                  """STOP IF JSON CAN'T BE LOADED"""

while True:
    sendatelegraph(PSST)                        """SEND FOREVER"""