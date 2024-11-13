from machine import Pin,I2C
from lib.bmp280 import *

#test_loop = 1      # Documented at EOF
#test_loop = 2      
#test_loop = 3      
#test_loop = 4      
#test_loop = 5      

class Probe:

    def __init__(self,bus,scl,sda,freq):
        #if __name__ =="__main__":
        #self.assign(parameter)
        self.bus = I2C(bus,scl=Pin(scl),sda=Pin(sda),freq=freq)
        self.bmp = BMP280(self.bus)
        self.bmp.use_case(BMP280_CASE_INDOOR)
        
    def pressure(self):
        pressure = self.bmp.pressure
        return pressure

    def temperature(self):
        temperature = self.bmp.temperature
        return temperature
    
    def reading(self):
        reading = (self.temperature(), self.pressure())
        return reading

if __name__ == "__main__":
    from utime import sleep

    if test_loop == 1:
        print("test 1")
        
        while True:
            bus = 0, 1, 0, 200000
            sensor = Probe(bus[0],bus[1],bus[2],bus[3])
            pressure=sensor.pressure()
            temperature=sensor.temperature()
            print("{} C {} Pa".format(temperature, pressure))
            utime.sleep(1)

    elif test_loop == 2:
        print("test 2")
        testbmp = Probe(0,1,0,200000)
        #testbmp.use_case(BMP280_CASE_INDOOR)

        while True:
            testpressure=testbmp.pressure()
            p_bar=testpressure/100000
            p_mmHg=testpressure/133.3224
            testtemperature=testbmp.temperature()
            testreading=testbmp.reading()
            print("{} degrees C {} Pascals {}".format(testtemperature, testpressure, testreading))
            utime.sleep(.07)
            
    elif test_loop == 3:
        print("test 3")
        for i in range(5):
            #bus = assign((0, 1, 0, 200000))
            sensor = Probe(0,1,0,200000)
            reading=sensor.reading()
            temperature=reading[1]
            pressure=reading[0]
            print("{} C {} Pa {}".format(temperature, pressure, reading))
            utime.sleep(.08)
            
    elif test_loop == 4:
        print("test 4")
        print("[  Temp  ]    [  bar  ]       [ time ]")
        print("[ /29.75 ]    [/1.036 ]       ")
        
        log=open("logs/log_4.csv","w")
        log.write("Temperature (C),Pressure (bar),Time"+'\n')
        log.close()
        while True:
            bus = 0, 1, 0, 200000
            sensor = Probe(bus[0],bus[1],bus[2],bus[3])
            reading=sensor.reading()
            temperature=reading[0]
            pressure=reading[1]
            p_bar=pressure/100000
            p_mmHg=pressure/133.3224
            time=str(utime.localtime()[3])+":"+str(utime.localtime()[4])+":"+str(utime.localtime()[5])

            print(f"{temperature:.4} C       {p_bar/1.003657:.4} bar        {time}")#        {utime.localtime()[3]:02d}:{utime.localtime()[4]:02d}:{utime.localtime()[5]:02d}")
            log=open("logs/log_4.csv","a")
            log.write(str(temperature)+","+str(p_bar)+","+str(time)+'\n')
            log.close()

            utime.sleep(.5)
            
    elif test_loop == 5:
        print("test 5")
        log=open("logs/log_5.csv","w")
        log.write("Temperature"+","+"Pressure"+'\n')
        log.close()
        print(" [ Temp ]   [  Pa  ]")
        for i in range (10):
            bus, scl, sda, freq = 0, 1, 0, 200000
            directbus = I2C(bus,scl=Pin(scl),sda=Pin(sda),freq=freq)
            bmpsensor = BMP280(directbus)
            bmpsensor.use_case(BMP280_CASE_INDOOR)
            pressure=bmpsensor.pressure
            temperature=bmpsensor.temperature
            print(" {} C    {} Pa".format(temperature, pressure))
            log=open("logs/log_5.csv","a"+'\n')
            log.close()
            log.write(str(temperature)+","+str(pressure))
            utime.sleep(0.1)
"""
Test loop reference:

test_loop = 1      # Fn call w/parameters passed in variable, separate readings   #PASSED
test_loop = 2      # Fn call w/hard parameters, separate and combined readings    #PASSED
test_loop = 3      # Fn call, returns combined reading which is then separated    #PASSED
test_loop = 4      # Fn call, w/variables, returns combined and separates, logs   #PASSED
test_loop = 5      # Direct library call with hard use_case

"""