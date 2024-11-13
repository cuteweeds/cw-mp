from machine import ADC, RTC
import time
afdc = machine.ADC(4)
rtc = machine.RTC()
while True:
    ADC_voltage = adc.read_u16() * (3.3 / (65535))
    temp_c = 27 - (ADC_voltage - 0.706)/0.001721
    t_now = rtc.datetime()
    t_readout = str(t_now[0]) + '/' + str(t_now[1]) + "/" + str(t_now[2]) + " " + str(t_now[4]) + ":" + str(t_now[5])
    print('Temp.: {}°C @ {}'.format(temp_c,t_readout))
    time.sleep_ms(300000)