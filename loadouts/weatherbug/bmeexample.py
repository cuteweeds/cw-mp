from machine import Pin, I2C        #importing relevant modules & classes
from time import sleep
import bmedriver       #importing BME280 library
 
i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)    #initializing the I2C method 
 
 
while True:
  bme = bmedriver.BME280(i2c=i2c)          #BME280 object created
  print(bme.values)
  sleep(1)           #delay of 10s