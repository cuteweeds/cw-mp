from machine import Pin, ADC
from utime import sleep

test=0

class LDR:
    def __init__(self,pin):
        self.pin=ADC(pin)
    def get_raw_reading(self):
        return self.pin.read_u16()
    def reading(self):
        return round(self.get_raw_reading()/65535,2)*100


if __name__=="__main__":
    if test==0:
        ldr=LDR(28)
        while True:
            print(ldr.reading())
            sleep(.1)
            
    if test==1:
        led=Pin("LED",Pin.OUT)
        red=Pin(12,Pin.OUT)
        ldrpin=28

        red.off()
        led.on()
        sleep(1)

        calibration = ADC(ldrpin).read_u16()
        print(calibration)

        while True:
            lightval=ADC(28).read_u16()
            if lightval < calibration-500:
                red.on()
            else:
                red.off()
                led.off()
            sleep(.1)
            print(lightval)