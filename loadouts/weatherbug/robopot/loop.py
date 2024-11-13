import bmedriver
import picotemperature
from machine import Pin, I2C, ADC, RTC
from time import sleep

# Initializing the I2C method 
i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)

# Initializing the internal thermometer and RTC
adc = ADC(4)
rtc = RTC()
ADC_temp_baseline = 17.03673
ADC_calibrated_flag = 0
iterations = 0
recalibrate_cycle = 10000
timer = 0

while True:
    # BME280 object created
  bme = bmedriver.BME280(i2c=i2c)          
  print(bme.values)
  
  # ADC object created and read
  ADC_voltage = adc.read_u16() * (3.3 / (65535))
  temp_c = ADC_temp_baseline - (ADC_voltage - 0.706)/0.001721
  
  # recalibrate ADC
  if ADC_calibrated_flag == 0:
      calibration = bme.read_compensated_data()[0]/100-temp_c
      ADC_temp_baseline = ADC_temp_baseline + calibration
      if calibration < 0.1:
          iterations += 1
      if iterations > 10:
          ADC_calibrated_flag = 1
          iterations = 0
          timer = time.ticks_ms
  else:
      if time.ticks_ms() - timer > recalibrate_cycle:
          ADC_calibrated_flag = 0



      


  # datetime read
  t_now = rtc.datetime()
  
  #output
  print(bme.values)
  t_readout = str(t_now[0]) + '/' + str(t_now[1]) + "/" + str(t_now[2]) + " " + str(t_now[4]) + ":" + str(t_now[5])
  print('Temp.: {}°C @ {}'.format(temp_c,t_readout))
  

  
  sleep(2)