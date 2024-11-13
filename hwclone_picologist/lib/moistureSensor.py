from machine import Pin, ADC
from utime import sleep_ms

max = 65535 ; drypoint= 45000 ; wetpoint = 18000 ; valrange = drypoint- wetpoint
testloop = 1

class moisture:
    
    # Calibrated constants
    drypoint = 35000
    wetpoint = 18000
    valrange = drypoint- wetpoint
    
    def __init__(self,pin):
        self.pin = pin
            
    def reading(self):
        reading = compress(read(100,self.pin))
        moisture = round(1 - (reading - wetpoint) / valrange, 2 ) * 100
        return(moisture)
        
def read(interval, pin):
    sleep_ms(interval)
    raw = ADC(pin).read_u16()
    return raw

# report readings under low point as low, over high point as high
def compress(raw):         
    if raw < wetpoint: raw = wetpoint;
    if raw > drypoint: raw = drypoint;
    return raw

if __name__ == "__main__":
    if testloop == 1:
        soil1 = 27
        while True:
            reading = compress(read(100,soil1))
            moisture = round(1 - (reading - wetpoint) / valrange, 2 ) * 100
            print(f'moisture: {moisture:2}% ') 
            if moisture < 40:
                print('dry')
                
    if testloop == 2:
        probe = Probe("glass",26)
        try:
            reading = probe.poll()
            assert reading > 0 and reading < 10
        except:
            print("bad sensor reading")