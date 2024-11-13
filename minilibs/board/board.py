### IDs micropython boards and their pins and properties from a set list
###
### simple invocations:
###
###    from board import boardID
###
###     Board = boardID()
###     print("Detected " + Board.type)
### 
###     for key, value in Board.Pins.items():
###         print(key, value)


import sys
import os
from utime import sleep_ms

class boardID:
    def __init__(self):
        self.type = self.detect_board_type()
        if self.type == 'RPi Pico':
            ### RPi Pico ###
            self.Pins = {
                'GROUND' : {3,8,13,18,23,28,38},
                'VBUS' : 40,
                'VSYS' : 39,
                'V3EN' : 37,
                'V3OUT' : 36,
                'ADC_VREF' : 35,
                'ADC_GND' : 33,
                'RUN' : 30,
                
                'GP0' : 1,
                'SPI0RX' : 1,
                'I2C0SDA' : 1,
                'UART0TX' : 1,
                
                'GP1'   : 2,
                'SPI0CS'  : 2,
                'I2C0SCL'  : 2,
                'UART0TX' : 2,
                
                'GP2'   : 4,
                'SPI0SCK'  : 4,
                'I2C1SDA'  : 4,
                
                'GP3' : 5,
                'SPI0TX'  : 5,
                'I2C1SCL' : 5,
                
                'GP4'   : 6,
                'SPI0RX'  : 6,
                'I2C0SDA' : 6,
                'UART1TX' : 6,
                
                'GP5'   : 7,
                'SPI0CS'  : 7,
                'I2C0SCL' : 7,
                'UART1RX' : 7,
                
                'GP6'   : 9,
                'SPI0SCK' : 9,
                'I2C1SDA' : 9,
                
                'GP7'   : 10,
                'SPI0TX'  : 10,
                'I2C1SCL' : 10,

                'GP8' : 11,
                'SPI1RX' : 11,
                'I2C0SDA' : 11,
                'UART1TX' : 11,
                
                'GP9'   : 12,
                'SPI1CS'  : 12,
                'I2C0SCL' : 12,
                'UART1RX' : 12,
                
                'GP10' : 14,
                'SPI1SCK' : 14,
                'I2C1SDA' : 14,
                
                'GP11' :  15,
                'SPI1TX' : 15,
                'I2C1SCL' : 15,
                
                'GP12' : 16,
                'SPI1RX' : 16,
                'I2C0SDA' : 16,
                'UART0TX' : 16,
                
                'GP13' : 17,
                'SPI1CS' : 17,
                'I2C0SCL' : 17,
                'UART0RX' : 17,
                
                'GP14' : 19,
                'SPI1SCK' : 19,
                'I2C1SDA' : 19,
                
                'GP15' :  20,
                'SPI1TX' : 20,
                'I2C1SCL' : 20,
                
                'GP16' : 21,
                'SPI0RX' : 21,
                'I2C0SDA' : 21,
                'UART0TX' : 21,
                
                'GP17' : 22,
                'SPI0CS' : 22,
                'I2C0SCL' : 22,
                'UART0RX' : 22,
                
                'GP18' : 24,
                'SPI0SCK' : 24,
                'I2C1SDA' : 24,
                
                'GP19' : 25,
                'SPI0TX' : 25,
                'I2C1SCL' : 25,
                
                'GP20' : 26,
                'SPI0RX' : 26,
                'I2C0SDA' : 26,
                
                'GP21' : 27,
                'SPI0CS' : 27,
                'I2C0SDA' : 27,
                'UART1RX' : 27,
                
                'GP22' : 29,
                
                'GP26' : 31,
                'A0' : 31,
                'SPI1SCK' : 31,
                'I2C1SDA' : 31,
                
                'GP27' : 32,
                'A1' : 32,
                'SPI1TX' : 32,
                'I2C1SCL' : 32,
                
                'GP28' : 34,
                'A2' : 34,
                'SPI1RX' : 34,
                
                'wifi' : 'no'
                }
        
    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine = os.uname().machine.lower()

        if sysname == 'rp2' and 'pico with' in machine:
            return 'RPi Pico'
        elif sysname == 'rp2' and 'pico w ' in machine:
            return 'RPi Pico W'
        elif sysname == 'esp8266':
            return 'ESP8266'
        # Add more conditions for other boards here
        else:
            return 'Unknown'

if __name__=="__main__":
    Board = boardID()
    print("Detected " + Board.type)

    for key, value in Board.Pins.items():
        print(key, value)