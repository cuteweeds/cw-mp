from ssd1306 import SSD1306_I2C
from machine import Pin, I2C

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

if __name__ == "__main__":
    oled.text("leila is cool", 10, 10)
    oled.show()