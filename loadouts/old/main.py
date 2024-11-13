from ST7735.ST7735 import TFT
from ST7735.sysfont import sysfont
import lib.config.default as CFG
from machine import SPI, Pin, RTC
from utime import localtime, sleep_ms, ticks_ms

# CHECK BOOT DATE AND TIME
local_no_NTP = localtime()
rtc_no_NTP = RTC().datetime()

# INIT WIFI
if CFG.WIFI_ON == True:
    #from NRF24L01.nrf24l01 import NRF24L013
    pass

# Display options
bevel = 2             # unused
fontsize = 2
padding = 3
lines = 8            # Vertical steps per cycle
fade_cap = 2          # Iterations of fadeout (higher = slower refresh rate)

# Colors
r,g,b =255,80,160
dark = 1 ; dim = 2 ; normal = 1 ; shift = 80

bevel = "off"          # unused
debug = "off"          # "color", "position", or "off"
highlight = "on"       # "on": color bar in bg ; "off": none
notxt = False          # False = render time ; True = keep display blank (for testing)
h_off = False          # Text doesn't move horizontally

# Device setup
Pico_SCK = CFG.SPI1_SCK
Pico_SDA = CFG.SPI1_COPI
Pico_A0_ = CFG.SPI1_A0
Pico_RES = CFG.SPI1_RESET
Pico_CS_ = CFG.SPI1_CS
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(Pico_SCK), mosi=Pin(Pico_SDA), miso=None)
tft=TFT(spi,Pico_A0_,Pico_RES,Pico_CS_)
tft.initr()
tft.rgb(True)
horizontal = tft.size()[0]
vertical = tft.size()[1]
v = 0 ; t0 = 0 ; t1 = 0 ; t2 = 0 ; v0 = 0 ; v1 = 0 ; v2 = 0
v_offset = vertical//lines
textwidth = fontsize * sysfont["Width"] * 7
h_play = horizontal - textwidth
h_offset = h_play//lines
x_fade = 0 ; y_fade = 0
color = TFT.BLACK
rshift,gshift,bshift=shift//lines,-shift//lines,shift//(lines//2)

# Precalculate x and y coords as separate sets
h_coords = []                 
v_coords = []
for i in range(lines):
    h_coords.append(i*h_offset)
    v_coords.append(i*v_offset)

# Functions
def currenttime():
    hour = localtime()[3]
    minute = "%02d" % localtime()[4]
    second = "%02d" % localtime()[5]
    return f" {hour}:{minute} "

def r_increment():
    global r,rshift
    if 1 > r+rshift or r+rshift > 254:
        rshift = -rshift
    r += rshift
    
def g_increment():
    global g,gshift
    if 1 > g+gshift or g+gshift > 254:
        gshift = -gshift
    g += gshift

def b_increment():
    global b,bshift
    if 1 > b+bshift or b+bshift > 254:
        bshift = -bshift
    b += bshift

# Blank screen
tft.fill(TFT.BLACK)

while True:
    for t in range(lines):
        text = currenttime()
        if h_offset > 0:
            step = t
        else:
            step = lines - 1 - t
        # Fetch x and y coords
        x = h_coords[step]
        y = v_coords[step]
        if h_off == True:
            x = 0
        # Draw background
        if highlight == "on":
            tft.fillrect((0,y),(horizontal,fontsize*sysfont["Height"]),tft.color(r//normal,g//normal,b//normal))
            tft.fillrect((x,y),(textwidth+2*padding,fontsize*sysfont["Height"]),TFT.BLACK)
        # Draw text
        if notxt == False:
            tft.text((x, y), text, tft.color(r//normal, g//normal, b//normal), sysfont, fontsize, nowrap=True)
            #tft.text((x+bevel, y+bevel), text, tft.color(r//dark, g//dark, b//dark), sysfont, fontsize, nowrap=True)
        # Fade previous passes
        if notxt == False and t > 0:
            if h_offset > 0:
                for fadeout in range(t+1):
                    x_fade = h_coords[step-fadeout]
                    y_fade = v_coords[step-fadeout]

                    if h_off == True:
                        x_fade = 0
                    if fadeout < fade_cap:
                        tft.text((x_fade,y_fade), text, tft.color(r//(1+fadeout), g//(1+fadeout), b//(1+fadeout)), sysfont, fontsize, nowrap=True)
                    if highlight == "on" and fadeout < 6:
                        tft.fillrect((0,y_fade),(x_fade,fontsize*sysfont["Height"]),tft.color(r//(1+fadeout),g//(1+fadeout),b//(1+fadeout)))
                        tft.fillrect((x_fade+textwidth+2*padding,y_fade),(horizontal-x_fade-textwidth-padding,fontsize*sysfont["Height"]),tft.color(r//(1+fadeout),g//(1+fadeout),b//(1+fadeout)))
            else:
                for fadeout in range(t+1):
                    x_fade = h_coords[step+fadeout]
                    y_fade = v_coords[step+fadeout]
                    if h_off == True:
                        x_fade = 0
                    if fadeout < fade_cap:
                        tft.text((x_fade,y_fade), text, tft.color(r//(1+fadeout), g//(1+fadeout), b//(1+fadeout)), sysfont, fontsize, nowrap=True)
                    if highlight == "on" and fadeout < 6:
                        tft.fillrect((0,y_fade),(x_fade,fontsize*sysfont["Height"]),tft.color(r//(1+fadeout),g//(1+fadeout),b//(1+fadeout)))
                        tft.fillrect((x_fade+textwidth+2*padding,y_fade),(horizontal-x_fade-textwidth-padding,fontsize*sysfont["Height"]),tft.color(r//(1+fadeout),g//(1+fadeout),b//(1+fadeout)))
        
        # Loop debug
        if debug == "color":
            print(r,g,b)
        if debug == "position":
            if t > 0:
                print(step,": ",x,y) #," fade: ",x_fade,y_fade)
            else:
                print(step,": ",x,y)                    
        # Increment colors
        r_increment()
        g_increment()
        b_increment()
        
        # End of one downward or upward pass
        
    # Flip direction
    h_offset = -h_offset ; v_offset = -v_offset ; bevel = bevel
    
    # Debug @ flip
    if debug == "color":
        if h_offset > 0:
            pass #print(" /\ /\ /\ ")
        else:
            pass # print(" \/ \/ \/ ")
    if debug == "position":
        pass #print("flipped")