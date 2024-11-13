from machine import Pin, ADC
import utime

soil1 = ADC(26)
led = Pin("LED",Pin.OUT)
vcc = Pin(14,Pin.OUT)

max = 65535
dry = 45000
wet = 18000
range = dry - wet

def read(interval):
    utime.sleep_ms(interval)
    raw = soil1.read_u16()
    return raw

def compress(raw):         # report readings under low point as low, over high point as high
    if raw < wet:
        raw = wet
    if raw > dry:
        raw = dry
    return raw

while True:
    #reading = compress(dry1, wet1, read(50))
    reading = compress(read(100))
    moisture = f'{ round(1 - (reading - wet)/range,2):%}'
    print(moisture)