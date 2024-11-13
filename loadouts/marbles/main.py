import cfg as CFG
from machine import Pin, I2C, SPI, PWM, RTC
from utime import localtime, sleep_ms, ticks_ms
from random import randint
from mpu6050.imu import MPU6050
"""constants"""
accel_threshold = 0.3
color_positive = 0
blink = 20
subliminizer = randint(20,100)
screentype = "TFT"
"""initialize classes"""
if screentype=="OLED":
    from ssd1306 import SSD1306_I2C
    rect = {"width" : 4, "height" : 4}
    screen = {"width" : 128, "height" : 32}
    default_awake_ms = 4000
    rotational_threshold = 20
    topspeed = 8
    display_addr = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    display = SSD1306_I2C(screen["width"], screen["height"], display_addr)
    marblecolor=1
elif screentype=="TFT":
    from ST7735.ST7735 import TFT
    from ST7735.sysfont import sysfont
    r,g,b=127,0,255
    rect = {"width" : 12, "height" : 12}
    screen = {"width" : 128, "height" : 160}
    default_awake_ms = 1000
    rotational_threshold = 10
    topspeed = 8
    spi1 = SPI(1,baudrate=10000_000,
          polarity=0,
          phase=0,
          sck=Pin(CFG.tft_SCK),
          mosi=Pin(CFG.tft_SDA),
          miso=None)
    display = TFT(spi1, CFG.tft_A0_, CFG.tft_RES, CFG.tft_CS_)
    display.initr()
    display.rgb(True)
    display.fill(TFT.BLACK)
mpu_addr = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(mpu_addr)
"""state variables"""
#color shift variables
max_backlight = 65535 # mid: 32768 max: 65535
glow = 1.00
pwm = PWM(Pin(CFG.tft_BL))
pwm.freq(1000)
pwm.duty_u16(int(glow * max_backlight))
colorphase = 1
colorphases = ["r+","g+","r-","b+","g-","r+","b-"]
colorstep = 5
#mode step variables
waketime = default_awake_ms
state = 3
counter = 0
#motion varioables
velocity_x, velocity_y = 6, 6
roll, pitch = 0,0
x, y = int(screen["width"]/2 - rect["width"]/2), int(screen["height"]/2 - rect["height"]/2)
gx,gy,gz=0,0,0
t_start, t = ticks_ms(), ticks_ms()
def powersave():
    if screentype=="OLED":
        display.poweroff()
    else:
        pass
def delta(a,b):
    return a - b
def blank():
    if screentype=="OLED":
        display.fill_rect(0, 0, screen["width"], screen["height"], 0)  
        display.show()
    elif screentype=="TFT":
        sleep_ms(20)
        if velocity_x>0:
            x_origin = x
            blank_width = rect["width"]
        else:
            x_origin = x+rect["width"]
            blank_width = -rect["width"]+1
        if velocity_y>0:
            y_origin = y
            blank_height = rect["height"]
        else:
            y_origin = y + rect["height"]
            blank_height = -rect["height"]+1
        display.fillrect((x_origin,y_origin),(blank_width,velocity_y),TFT.BLACK)
        display.fillrect((x_origin,y_origin),(velocity_x,blank_height,),TFT.BLACK)
def invert_screen(reps):
    global color_positive, screentype
    if screentype == "OLED":
        for rep in range(reps):
            color_positive = not color_positive
            display.invert(color_positive)
            sleep_ms(blink)
    else:
        pass
def glimmer(a,mode):
    """changes glow, a factor used to set screen brightness, in response to acceleration or motionlessness"""
    global max_backlight, glow
    if mode == 0:
        glow = max(0,glow-0.005)
    else:
        glow = min(glow+int(a/200),1)
    if glow * max_backlight < 3000:
        glow=0
    return glow
def colorshift():
    global r,g,b,colorphase,colorphases,colorstep,velocity_x,velocity_y
    n = colorphases[colorphase % len(colorphases)]
    if n == "r+":
        r+=colorstep
        if 255<=r:
            r=255
            colorphase+=1
    if n == "r-":
        r-=colorstep
        if r<=0:
            r=0
            colorphase+=1
    if n == "g+":
        g+=colorstep
        if 255<=g:
            g=255
            colorphase+=1
    if n == "g-":
        g-=colorstep
        if g<=0:
            g=0
            colorphase+=1
    if n == "b+":
        b+=colorstep
        if 255<=b:
            b=255
            colorphase+=1
    if n == "b-":
        b-=colorstep
        if b<=0:
            b=0
            colorphase+=1
    colorstep = int((abs(velocity_x) + abs(velocity_y))/2)
def mode_picker(roll, pitch, ∆t):
    global counter, default_awake_ms, waketime, state, x, y, velocity_x, velocity_y
    nudge = (roll>0)|(pitch>0)
    if nudge == 0:
        waketime -= ∆t
        if waketime < 0:
            state -= 1
            waketime = default_awake_ms
            counter = 0
    else:
        waketime = default_awake_ms
        counter +=1
        if state == 0:
            if screentype=="OLED":
                display.poweron()
            else:
                pass
    if screentype == "TFT":
        glow = glimmer(abs(mpu.gyro.x)+abs(mpu.gyro.y),nudge)
        pwm.duty_u16(int(glow * max_backlight))
    if counter > 39:
        state = 3
    if 0 < counter < 40:
        state = 2
    if state == 3:
        marble()
    if state == 2:
        if velocity_x == 0:
            if (screen["width"]-rect["width"])<=x:
                velocity_x +=2
            else:
                velocity_x -=2
        if velocity_y == 0:
            if (screen["height"]-rect["height"])<=y:
                velocity_y +=2
            else:
                velocity_y -=2
        kinect_pong()
    if state == 1:
        pong()
    if state < 1:
        if screentype == "OLED":
            state = 0
            powersave()
        else:
            state = 1
def pong():
    """non-interactive pixel bounce"""
    global x, y, velocity_x, velocity_y,r,g,b
    if 0 < x+velocity_x < screen["width"] - rect["width"]:
        pass
    else:
        velocity_x = -velocity_x
        if screentype=="OLED":
            invert_screen(0)
    if 0 < y+velocity_y < screen["height"] - rect["height"]:
        pass
    else:
        velocity_y = -velocity_y
        if screentype=="OLED":
            invert_screen(0)
    blank()
    x += velocity_x
    y += velocity_y
    if screentype=="OLED":
        display.fill_rect(x, y, rect["width"], rect["height"], marblecolor)
        display.show()
    elif screentype=="TFT":
        colorshift()
        display.fillrect((x,y),(rect["width"],rect["height"]),display.color(r,g,b))
def kinect_pong():
    """interactive pixel bounce"""
    global x, y, velocity_x, velocity_y, roll, pitch
    if 0 < x+velocity_x < screen["width"] - rect["width"]:
        pass
    else:
        velocity_x = -velocity_x
    if 0 < y+velocity_y < screen["height"] - rect["height"]:
        pass
    else:
        velocity_y = -velocity_y
    tilt_x = int(roll/7)
    tilt_y = int(pitch/5)
    velocity_x += tilt_x
    velocity_y += tilt_y
    if velocity_x > topspeed:
        velocity_x = topspeed
    if velocity_y > topspeed:
        velocity_y = topspeed
    blank()
    x += velocity_x
    y += velocity_y
    if x < screen["width"] - rect["width"]:
        pass
    else:
        x = screen["width"] - rect["width"]
    if x > 0:
        pass
    else:
        x = 0
    if y < screen["height"] - rect["height"]:
        pass
    else:
        y = screen ["height"] - rect["height"]
    if y > 0:
        pass
    else:
        y = 0
    if screentype=="OLED":
        display.fill_rect(x, y, rect["width"], rect["height"], 1)
        display.show()
    elif screentype=="TFT":
        colorshift()
        display.fillrect((x,y),(rect["width"],rect["height"]),display.color(r,g,b))
def marble():
    """what if you had a little marble?"""
    global x, y, velocity_x, velocity_y, roll, pitch
    """correct inputs and limit speed"""
    tilt_x = int(roll/7)
    tilt_y = int(pitch/5)
    velocity_x += tilt_x
    velocity_y += tilt_y    
    if topspeed*2 < velocity_x:
        velocity_x = int(topspeed*2)
    if velocity_x < -topspeed*2:
        velocity_x = -int(topspeed*2)
    if topspeed*2 < velocity_y:
        velocity_y = int(topspeed*2)
    if velocity_y < -topspeed*2:
        velocity_y = -int(topspeed*2)
    blank()
    """bounce"""    
    if x < 0:
        x=0
        velocity_x = 0
        blank()
    if x+velocity_x > screen["width"] - rect["width"]:
        x = screen["width"] - rect["width"]
        velocity_x = 0
        blank()
    if y+velocity_y < 0:
        y=0
        velocity_y = 0
        blank()
    if y > screen["height"] - rect["height"]:
        y = screen["height"] - rect["height"]
        velocity_y = 0
        blank()
    x += velocity_x
    y += velocity_y
    if screentype=="OLED":
        display.fill_rect(x, y, rect["width"], rect["height"], 1)
        display.show()
    elif screentype=="TFT":
        colorshift()
        display.fillrect((x,y),(rect["width"],rect["height"]),display.color(r,g,b))
while True:    
    gx0 = gx
    gy0 = gy
    gz0 = gz
    t0 = t
    gx=round(mpu.gyro.x,1)
    gy=round(mpu.gyro.y,1)
    gz=round(mpu.gyro.z,1)
    t = ticks_ms()
    """insert sneaky messages"""
    now = int(round((t - t_start)/10,0))
    if now % subliminizer == 0:
        text="leilaiscool"
        row = randint(0,int(screen["width"]-len(text)*8))
        col = randint(0,int(screen["width"]-len(text)*8))
        if screentype=="OLED":
            display.text(text,row,col)
    ∆t = delta(t,t0)
    """velocity calculations (accept inputs only if angular acceleration > rotational_threshold)"""
    if abs(gx) > rotational_threshold:
        roll += round(∆t/1000 * gx,0)
    else:
        roll = 0
    if abs(gy) > rotational_threshold/4:
        pitch -= round(∆t/1000 * gy, 0)
    else:
        pitch = 0
    """do the thing"""
    mode_picker(roll, pitch, ∆t)