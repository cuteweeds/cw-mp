from machine import ADC, Pin
import time

led = Pin("LED",Pin.OUT)
soil_adc = ADC(26)

while True:
    moisture = soil_adc.read_u16()
    print(moisture)
    time.sleep_ms(50)