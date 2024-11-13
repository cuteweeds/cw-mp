import machine
from machine import Pin, SPI
from sdcard import SDCard
import uos
import time
import sd_config

# Local variables for pin assigments
SCK = sd_config.SCK
PICO = sd_config.PICO
POCI = sd_config.POCI
CS = sd_config.CS
led = machine.Pin("LED",Pin.OUT)

sd_spi = SPI(1, sck=Pin(SCK, Pin.OUT), mosi=Pin(PICO, Pin.OUT),
             miso=Pin(POCI, Pin.OUT))
sd = SDCard(sd_spi, Pin(CS, Pin.OUT))
sd.init_spi(10_000_000)  # speedup, from danjperron
vfs = VfsFat(sd)
mount(vfs, "/sd")

def blink(count, interval):
    for x in range(count):
        led.toggle()
        time.sleep_ms(interval)
    led.off()

led.on()

# Create a file and write something to it
with open("/sd/data.txt", "w") as file:
    print("Writing to data.txt...")
    file.write("Welcome to microcontrollerslab!\r\n")
    file.write("This is a test\r\n")
    blink(6,500)

# Open the file we just created and read from it
with open("/sd/data.txt", "r") as file:
    print("Reading data.txt...")
    data = file.read()
    print(data)
    blink(4,200)
