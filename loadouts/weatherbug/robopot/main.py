## TODO
## - Make temp max and min meaningful (low priority)


## Base modules

from machine import ADC, RTC, I2C, Pin
import time
import os

## Hardware-specific

import robopot.board as board

## Import sensors

import bmedriver
import robopot.moisture

## Initialize objects and methods
        
soil_adc = machine.ADC(26)
i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)    #initializing the I2C method
bme = bmedriver.BME280(i2c=i2c)
temp_adc = machine.ADC(4)
rtc = machine.RTC()


## Baselines

ADC_temp_baseline = 27
calibration = 0
error_range = [0, 0, 0]
count = 0
m_avg = 0
time_now = rtc.datetime()
tempvar_avg = 0
time_str = ""

## Functions

def readADC():  # ADC object created and read
    ADC_voltage = temp_adc.read_u16() * (3.3 / (65535))
    temp_onboard = ADC_temp_baseline - (ADC_voltage - 0.706)/0.001721

def calibrate(primary, secondary):
    global ADC_temp_baseline, calibration
    calibration = primary - secondary
    ADC_temp_baseline = ADC_temp_baseline + calibration
    return calibration

def obt_readout():
    global time_str
    time_str = str(time_now[0]) + '/' + str(f"{time_now[1]:02d}") + "/" + str(time_now[2]) + " " + str(time_now[4]) + ":" + str(f"{time_now[5]:02d}")
    #print(f'Temp.: {temp_onboard:02f}°C or {temp_bme} @ {time_str} ({calibration:02f})')
    return time_str

def monitor(calibration):
    global error_range, tempvar_avg
    if calibration < error_range[0]:
        error_range[0] = calibration
    elif calibration > error_range[1]:
        error_range[1] = calibration
    error_range[2] = round ( (error_range[2] + calibration) / x , 2 )
    #print(f'{temp_bme:0.0f}, {temp_onboard:0.0f} {tempvar_avg:0.4f}, {error_range[0]:0.4f}, {error_range[1]:0.4f}')
    #return value, error_range


## Calibrate BME280

print('\nCalibrating temperature sensors')
# print('\nt_bme, t_adc, var, avg_var')        # add column headers (if outputting calibration data)

for x in range(100):
    
    # Read sensor pair
    ADC_voltage = temp_adc.read_u16() * (3.3 / (65535))
    temp_onboard = ADC_temp_baseline - (ADC_voltage - 0.706)/0.001721    
    temp_bme = bme.read_compensated_data()[0]/100
    
    # Measure variance (primary sensor is datum)
    calibrate(temp_bme,temp_onboard)
    tempvar_avg = (tempvar_avg + calibration) / (x+1)
    #print(f'{temp_bme:0.2f}, {temp_onboard:0.2f}, {calibration:0.2f}')
    
    # Measure error range (discard first 3 readings)
    if x > 3:
        #print(temp_bme, tempvar_avg, calibration)
        monitor(calibration)
        #print(f'{temp_bme:0.2f}, {temp_onboard:0.2f}, {calibration:0.2f},  {tempvar_avg:0.2f}')   # Compare sensor variances
    time.sleep_ms(50)

print(f' Temperature: {temp_bme:0.2f}\n Secondary Temp: {temp_onboard:0.4f}\n Low error: {error_range[0]:0.4f}\n High error: {error_range[1]:0.4f}')


## Main Loop
while True:
    count += 1
    
    time_now = rtc.datetime()
    clock = obt_readout()
    
    ADC_voltage = temp_adc.read_u16() * (3.3 / (65535))
    temp_onboard = ADC_temp_baseline - (ADC_voltage - 0.706)/0.001721
    
    temp_bme = bme.read_compensated_data()[0]/100
    
    moisture = round(robopot.moisture.read(50),0)
    print(f"{temp_bme:0.2f} °C, {moisture/100:.0%} rel. Hum @ {clock}")
    
    time.sleep_ms(30000)