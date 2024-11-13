from machine import Pin,PWM,ADC
import sys, urandom, math
buzzer=PWM(Pin(5))
r=Pin(10,Pin.OUT)
adc=ADC(4)
buzzer.duty_u16(0)
scale = {"G" : 392, "A": 440,"B": 494,"C": 523,"D": 587,"E": 659,"F": 698,"J": 784}
longscale = {
    "1": 261,
    "2": 278,
    "3": 294,
    "4": 311,
    "5": 330,
    "6": 350,
    "7": 370,
    "8": 392,
    "9": 415,
    "10": 440,
    "11":466,
    "12":493
    }
def play(music):
    for note in music:
        tone = scale.get(note)
        buzzer.freq(tone)
        machine.lightsleep(300)
#play("GBABAGGABCADCJFEEFBGJG")

def sweep(start,end,duration):
    buzzer.freq(start)
    for i in range(start,end):
        buzzer.freq+=i
        machine.lightsleep(duration/(end-start))
buzzer.duty_u16(0000)
#sweep(1000,2000,2000)

def cacophonyForClaire(endurance):
    for note in range(0,endurance):
        rnd = urandom.uniform(1,36)
        octave = math.ceil(rnd/12)
        nextnote = str(math.ceil(rnd/3))
        nextduration = int(round(urandom.uniform(200,1000)))
        tone = longscale.get(nextnote)*octave
        buzzer.freq(tone)
        machine.lightsleep(nextduration)

buzzer.duty_u16(14435)
cacophonyForClaire(10)
buzzer.duty_u16(0)
