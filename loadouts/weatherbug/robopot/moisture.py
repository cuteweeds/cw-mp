from machine import ADC, Pin
import time
import robopot.board as board

## Initialize objects and variables
soil_adc = ADC(26)
calibration_dry = int(44000)
calibration_wet = int(0)
wet_countdown = 5
m_avg = int(0)
m_sum = int(0)
led = Pin("LED",Pin.OUT)
led.off()
def read(interval):
    global calibration_dry, m_avg
    m_read = soil_adc.read_u16()
    m_calibrated = max ( 0, 100 - (m_read / calibration_dry) * 100)
    time.sleep_ms(interval)
    return float(m_calibrated)

def calibrate_dry():
    global calibration_dry, m_avg, m_sum
    for x in range (100):
        m_read = soil_adc.read_u16()
        time.sleep_ms(20)
        m_sum = m_sum + m_read
        m_avg = m_sum / (x+1)
        calibration_dry = m_avg
        if __name__ == "__main__":
            print(calibration_dry)
            return calibration_dry
        else:
            if (x+1)%50 == 0:
                led.toggle()
        
def calibrate_wet():
    global calibration_wet, m_avg, m_sum
    for x in range (100):
        m_read = soil_adc.read_u16()
        time.sleep_ms(20)
        m_sum = m_sum + m_read
        m_avg = m_sum / (x+1)
        calibration_wet = m_avg
        if __name__ == "__main__":
            print(calibration_wet)
            return calibration_wet
            
if __name__ == "__main__":    
    for x in range(100):
        dry = calibrate_dry()
        wet = calibrate_wet()
        moisture = read(50) / dry * 100
        print(moisture)


## Main program

else:
    led = board.set_pins()
    led.off()
    
    ## Test and calibrate dry point
    
    for x in range(3):
        test = read(50)
        
    if test < calibration_dry:
        led.on()
        print("Calibrating soil moisture sensor. Keep sensor dry.")
        
        calibrate_dry()
        
        print(f' Dry calibration complete @ {calibration_dry:,.0f}.')
        led.off()

    else:
        print(f"No calibration required. Dry baseline @ {test:,}.")
    
    
    ## Display instructions
        
    print(f'\nPlace sensor in water.\n Wet-point test begins in {wet_countdown}…', end='')
    
    while wet_countdown > 1:
        led.toggle()
        time.sleep_ms(1000)
        wet_countdown -= 1
        print(f'{wet_countdown}…', end='')
    led.off
    
    
    ## Test and calibrate wet point
    
    for x in range(3):
        test = read(50)
        
    if test > calibration_wet:
        led.on()
        print("\n\nCalibrating soil moisture sensor. Keep sensor wet.")
        
        m_sum, m_avg = 0, 0
        calibrate_wet()
        
        print(f' Wet calibration complete @ {calibration_wet}.')
        led.off()

    else:
        #m_avg = test
        led.on()
        time.sleep_ms(500)
        print(f"\nNo calibration required. Wet baseline @ {test}.")
        led.off()