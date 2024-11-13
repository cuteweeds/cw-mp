from machine import ADC, RTC, I2C, Pin
import time
import bmedriver
import robopot.board as board
import robopot.moisture

## Initialize objects and methods
        
soil_adc = machine.ADC(26)
temp_adc = machine.ADC(4)
rtc = machine.RTC()
i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)    #initializing the I2C method
bme = bmedriver.BME280(i2c=i2c)

## Sensor baselines

ADC_temp_baseline = 27
calibration = 0
error_range = [0, 0, 0]

## Functions

def readADC():  # ADC object created and read
    ADC_voltage = temp_adc.read_u16() * (3.3 / (65535))
    temp_onboard = ADC_temp_baseline - (ADC_voltage - 0.706)/0.001721

def calibrate():
    global ADC_temp_baseline, calibration
    calibration = bme.read_compensated_data()[0]/100 - temp_onboard
    ADC_temp_baseline = ADC_temp_baseline + calibration

def output():
    # datetime read
    t_now = rtc.datetime()

def obt_readout():
    time_str = str(t_now[0]) + '/' + str(f"{t_now[1]:02d}") + "/" + str(t_now[2]) + " " + str(t_now[4]) + ":" + str(f"{t_now[5]:02d}")
    print(f'Temp.: {temp_onboard:02f}°C or {temp_bme} @ {time_str} ({calibration:02f})')

def monitor(value):
    global error_range
    if count > 3:
        if calibration < error_range[0]:
            error_range[0] = calibration
        elif calibration > error_range[1]:
            error_range[1] = calibration
        error_range[2] = round ( (error_range[2]+calibration) / count , 2 )

count = 0
m_avg = 0

while True:
    count += 1
    
    ADC_voltage = temp_adc.read_u16() * (3.3 / (65535))
    temp_onboard = ADC_temp_baseline - (ADC_voltage - 0.706)/0.001721
    
    temp_bme = bme.read_compensated_data()[0]/100
    
#    moisture = soil_adc.read_u16()
#    m_tmp = ( m_avg + moisture )
#    m_avg = m_tmp / count
#    print(f"{moisture} {m_avg:0}")
    moisture = round(robopot.moisture.read(50),0)
    print(f"{moisture/100:0%}")
    
    t_now = rtc.datetime()
    
#    calibrate()
#    monitor(calibration)
#    print(f'{calibration:02f} Range: {error_range}')
    #obt_readout()
    
    time.sleep_ms(50)
