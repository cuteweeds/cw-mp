from machine import Pin, I2C, idle
from utime import sleep_ms, ticks_ms
from random import randint
from ssd1306 import SSD1306_I2C
from mpu6050.imu import MPU6050

"""constants"""
bgcolor = 0
blink = 20
accel_threshold = 0.3
rotational_threshold = 20
subliminizer = randint(20,100)

"""initialize classes"""
oled = {"width" : 128, "height" : 32}
rect = {"width" : 4, "height" : 4}
display_addr = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
display = SSD1306_I2C(oled["width"], oled["height"], display_addr)
mpu_addr = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
mpu = MPU6050(mpu_addr)

def delta(a,b):
    return a - b
def blank():
    display.fill_rect(0, 0, oled["width"], oled["height"], 0)
    display.show()
def invert_oled(reps):
    global bgcolor
    for rep in range(reps):
        bgcolor = not bgcolor
        display.invert(bgcolor)
        sleep_ms(blink)
def pong():
    """non-interactive pixel bounce"""
    global x, y, velocity_x, velocity_y
    display.fill_rect(x, y, rect["width"], rect["height"], 1)
    display.show()
    if 0 < x < oled["width"] - rect["width"]:
        pass
    else:
        velocity_x = -velocity_x
        invert_oled(0)
    if 0 < y < oled["height"] - rect["height"]:
        pass
    else:
        velocity_y = -velocity_y
        invert_oled(0)
    x += velocity_x
    y += velocity_y
    blank()
def kinect_pong():
    """interactive pixel bounce"""
    global x, y, velocity_x, velocity_y, roll, pitch
    blank()
    tilt_x = int(roll/7)
    tilt_y = int(pitch/5)
    velocity_x += tilt_x
    velocity_y += tilt_y
    if velocity_x > oled["width"]/2:
        velocity_x - int(oled["width"]/2)
    if 0 < x < oled["width"] - rect["width"]:
        pass
    else:
        velocity_x = -velocity_x
    if velocity_y > oled["height"]/4:
        velocity_x - int(oled["height"]/4)
    if 0 < y < oled["height"] - rect["height"]-1:
        pass
    else:
        velocity_y = -velocity_y
    x += velocity_x
    y += velocity_y
    display.fill_rect(x, y, rect["width"], rect["height"], 1)
    display.show()
def marble():
    """what if you had a little marble?"""
    global x, y, velocity_x, velocity_y, roll, pitch
    blank()
    tilt_x = int(roll/7)
    tilt_y = int(pitch/5)
    velocity_x += tilt_x
    velocity_y += tilt_y    
    x += velocity_x
    y += velocity_y
    if x < 0:
        x=0
        velocity_x = 0
    if x > oled["width"] - rect["width"]:
        x = oled["width"] - rect["width"]
        velocity_x = 0
    if y < 0:
        y=0
        velocity_y = 0
    if y > oled["height"] - rect["height"]:
        y = oled["height"] - rect["height"]
        velocity_y = 0
    display.fill_rect(x, y, rect["width"], rect["height"], 1)
    display.show()
    
def powersave():
    print("entering powersave")
    machine.idle()
    
    


"""state variables"""
velocity_x, velocity_y = 0, 0
roll, pitch, yaw = 0,0,0
x, y = int(oled["width"]/2 - rect["width"]/2), int(oled["height"]/2 - rect["height"]/2)
#ax=round(mpu.accel.x,1)
#ay=round(mpu.accel.y,1)
#az=round(mpu.accel.z,1)
gx=round(mpu.gyro.x)
gy=round(mpu.gyro.y)
gz=round(mpu.gyro.z)
#tem=round(mpu.temperature,2)
t_start, t = ticks_ms(), ticks_ms()

while True:    
    #ax0 = ax  """skipping unnecessary variables"""
    #ay0 = ay
    #az0 = az
    gx0 = gx
    gy0 = gy
    gz0 = gz
    #tem0 = tem
    t0 = t
    #ax=round(mpu.accel.x,1)
    #ay=round(mpu.accel.y,1)
    #az=round(mpu.accel.z,1)
    gx=round(mpu.gyro.x,1)
    gy=round(mpu.gyro.y,1)
    gz=round(mpu.gyro.z,1)
    #tem=round(mpu.temperature,2)
    t = ticks_ms()
    """insert sneaky messages"""
    now = int((t - t_start))
    if now % subliminizer == 0:
        row = randint(0,int(oled["width"]-80))
        col = randint(0,int(oled["width"]-80))
        display.text("leila is cool",row,col)
    """velocity calculations"""
#    ∆ax = delta(ax0,ax)
#    ∆ay = delta(ay0,ay)
#    ∆az = delta(az0,az)
    ∆t = delta(t,t0)
    """accept inputs only if angular acceleration is over threshold"""
    if abs(gx) > rotational_threshold:
        pitch -= round(∆t/1000 * gx,0)
    else:
        pitch = 0
    if abs(gy) > rotational_threshold/4:
        roll -= round(∆t/1000 * gy, 0)
    else:
        roll = 0
    if abs(gz) > rotational_threshold:
        yaw -= round(∆t/1000 * gz,0)
    else:
        yaw = 0
    """do the thing"""
    marble()
    print(Pin(1).value())
    #pong
    #kinect_pong