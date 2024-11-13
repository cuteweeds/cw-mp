import devices
import config.default as CFG
from ldr import LDR
from led import RGB, LED
from sense import resolution
from utime import ticks_ms, sleep, localtime
from machine import Pin, RTC
from bmp280reading import Probe as thermobaro
from moistureSensor import moisture
from ultrasoundSensor import hcsr04 as ultra


"""INITIALIZE OLED DISPLAY"""
# TODO: Improve text parameter handling to be more flexible
if CFG.OLED91_ON==True:
    from oled128x32 import display
    oled=display(CFG.OLED_BUS,CFG.OLED_SDA,CFG.OLED_SCL,CFG.OLED_FREQ,CFG.OLED_WIDTH,CFG.OLED_HEIGHT)
    oled.display.fill(0)        # Todo: Wrap
    oled.display.show()
    oled.display.text("PICOLOGIST",20,0)
    oled.display.text(CFG.BOARD_TYPE,0,12)
    oled.display.text("BT:    Wifi:   ",0,24)
    oled.display.show()
    sleep(1)
    #centre=int(4*(10-len(BOARD_TYPE)/2))   # TODO: Add text formatting to oled lib

    def onscreen(line1,line2,line3,line3r):
        try:
            oled.display.fill(0)
            oled.display.show()
            oled.display.text(line1,0,0)
            oled.display.text(line2,0,12)
            oled.display.text(line3,0,24)
            oled.display.text(line3r,86,24)
            oled.display.show()
        except:
            CFG.BLINK.pattern(5,.5,.25)
            sleep(.5)
            CFG.BLINK.pattern(5,.5,.25)
else:
    CFG.BLINK.pattern(5,1,.5)
    def onscreen(a,b,c,d):
        pass

serialBluetooth = devices.bluetooth(CFG.BLUETOOTH_ON)
if len(str(serialBluetooth)) > 20:
    try:
        oled.display.text("BT: On Wifi:   ",0,24)
        oled.display.show()
    except:
        pass
#WAN = devices.wifi(CFG.WIFI_ON, CFG.SSID, CFG.PASSWORD)
#connection = http.open_socket(WAN.ip)


"""CHECK BOOT DATE AND TIME"""
local_no_NTP = localtime()
rtc_no_NTP = RTC().datetime()

"""INIT WIFI"""
if CFG.WIFI_ON == True:
    import server.http as http
    Wi="Wifi"
else:
    Wi=""


# INITIALIZE WIFI AND SET TIME                    # TODO: auto reconnect Wifi
if CFG.WIFI_ON==True:
    print("Starting Wifi")
    WAN = http.wifi(CFG.SSID, CFG.PASSWORD)
    if WAN.ip == "0.0.0.0":
        CFG.WIFI_ON=False
        print("No IP: ",WAN.ip)
        print("Can't sync time. Using device default time")
        try:
            onscreen("Can't sync time.","Using default.","","")
            CFG.TZ=0
        except:
            pass
    else:
        connection=http.open_socket(WAN.ip)
        oled.display.text("BT:    Wifi: On",0,24)
        oled.display.show()
        sleep(.75)
        onscreen("Online:",WAN.ip,"","")
        import ntptime
        try:
            ntptime.settime()
            print("checking NTP")
        except:
            print("Can't contact time server.")
            CFG.TZ=0
            try:
                onscreen("Can't contact","time server.","","")
            except:
                pass
time = localtime()
rtc_NTP = RTC().datetime()
#local_NTP = localtime()
#time = local_NTP
print("log time: ",time)
if time[3] <= abs(CFG.TZ)-1:
    est_hour = 24+(CFG.TZ-time[3])
    hour = f"{est_hour:02}{time[4]:02}"
    f_hour = f"{est_hour:02}:{time[4]:02}"
    est_date = time[1]-1
    date = f"{time[0]}{est_date:02}{time[2]:02}"
    f_date = f"{time[0]-2000}{est_date:02}{time[2]:02}"
    
else:
    est_hour = time[3]-CFG.TZ
    hour = f"{est_hour:02}{time[4]:02}"
    f_hour = f"{est_hour:02}:{time[4]:02}"
    f_hour_RTC = f"{rtc_NTP[4]-CFG.TZ}:{rtc_NTP[5]:02}"
    date = f"{time[0]}{time[1]:02}{time[2]:02}"
    f_date = f"{time[0]-2000}{time[1]:02}{time[2]:02}"
timestamp = (date,hour)      
if f_date=="210101":
    logfile = "logs/log--nodate.csv"
else:
    logfile = "logs/log-"+f_date+"-"+hour+".csv"
print("Logfile name: ",logfile)
if CFG.WIFI_ON==True:
    onscreen("Online:",WAN.ip,f"Date: {date}","")
    #onscreen(f"L: {local_no_NTP[3]}:{local_no_NTP[4]:02} -> {f_hour}",f"R: {rtc_no_NTP[4]}:{rtc_no_NTP[4]} -> {f_hour_RTC}","","")
    #onscreen(f"Time: {f_hour}","","","")
    #onscreen(f"L: {f_hour}",f"R: {f_hour_RTC}","","")
    sleep(1)

"""
if CFG.WIFI_ON==True:
    print("Starting Wifi")
    WAN = http.wifi(CFG.SSID, CFG.PASSWORD)
    if WAN.ip == "0.0.0.0":
        WIFI_ON=False
        print("No IP: ",WAN.ip)
        print("Can't sync time. Using device default time")
        try:
            onscreen("Can't sync time.","Using default.","","")
            CFG.TZ=0
        except:
            pass
    else:
        connection=http.open_socket(WAN.ip)
        oled.display.text("BT: On Wifi: On",0,24)
        oled.display.show()
        sleep(.75)
        onscreen("Online:",WAN.ip,"","")
        print("checking NTP")
        try:
            ntptime.settime()
        except:
            print("Can't contact time server.")
            CFG.TZ=0
            try:
                onscreen("Can't contact","time server.","","")
            except:
                pass
            


if CFG.BLUETOOTH_ON == True:
    ble = bluetooth.BLE()
    serialBluetooth = BLESimplePeripheral(ble)
    oled.display.text("BT: On Wifi:   ",0,24)
    oled.display.show()
    print("Bluetooth on")
    CFG.BLINK.pattern(3,.25,.25)
    # DEFINE BLUETOOTH TRIGGERS
    def on_rx(data):
        print("Data received: ", data)
        global BOARD_LED_STATE                    # Variable(s) to be set by any incoming BT instructions
        if data == b'flick\r\n':                  # Setup keyword trigger(s) for incoming BT instructions
            led.value(not BOARD_LED_STATE)   
            BOARD_LED_STATE = 1 - BOARD_LED_STATE


CONFIRM CONNECTION FOR NTP
if WAN.ip == "0.0.0.0":
    print("Can't sync time. Using device default time")
    try:
        onscreen("Can't sync time.","Using default.","","")
        CFG.TZ=0
    except:
        pass
else:
    import ntptime
    oled.display.text("BT: On Wifi: On",0,24)
    oled.display.show()
    sleep(.75)
    onscreen("Online:",WAN.ip,"","")
    try:
        ntptime.settime()
    except:
        print("Can't contact time server.")
        CFG.TZ=0
        try:
            onscreen("Can't contact","time server.","","")
        except:
            pass
time = localtime()
rtc_NTP = RTC().datetime()
print("log time: ",time)
if time[3] <= abs(CFG.TZ)-1:
    est_hour = 24+(CFG.TZ-time[3])
    hour = f"{est_hour:02}{time[4]:02}"
    f_hour = f"{est_hour:02}:{time[4]:02}"
    est_date = time[1]-1
    date = f"{time[0]}{est_date:02}{time[2]:02}"
    f_date = f"{time[0]-2000}{est_date:02}{time[2]:02}"
else:
    est_hour = time[3]-CFG.TZ
    hour = f"{est_hour:02}{time[4]:02}"
    f_hour = f"{est_hour:02}:{time[4]:02}"
    f_hour_RTC = f"{rtc_NTP[4]-CFG.TZ}:{rtc_NTP[5]:02}"
    date = f"{time[0]}{time[1]:02}{time[2]:02}"
    f_date = f"{time[0]-2000}{time[1]:02}{time[2]:02}"
timestamp = (date,hour)      
if f_date=="210101":
    logfile = "logs/log--nodate.csv"
else:
    logfile = "logs/log-"+f_date+"-"+hour+".csv"
print("Logfile name: ",logfile)

if CFG.WIFI_ON==True:
    onscreen("Online:",WAN.ip,f"Date: {date}","")
    #onscreen(f"L: {local_no_NTP[3]}:{local_no_NTP[4]:02} -> {f_hour}",f"R: {rtc_no_NTP[4]}:{rtc_no_NTP[4]} -> {f_hour_RTC}","","")
    #onscreen(f"Time: {f_hour}","","","")
    #onscreen(f"L: {f_hour}",f"R: {f_hour_RTC}","","")
    sleep(1)
"""
    
# TODO: move Sensor() to lib
class sensor:
    def __init__(self,name,parameter):
        self.parameter = parameter
        self.name = name
        self.modules = {"moisture":moisture, "ultra":ultra, "thermobaro":thermobaro, "ldr":LDR}
        module = self.getmodule()
        if self.name == "moisture":
            self.id = module(self.parameter)
        if self.name == "ultra":
            trigger = self.parameter[0]
            echo = self.parameter[1]
            self.id = module(trigger,echo)
        if self.name == "thermobaro":
            self.bus=parameter[0]
            self.scl=parameter[1]
            self.sda=parameter[2]
            self.freq=parameter[3]
            self.id = module(self.bus, self.scl, self.sda, self.freq)
        if self.name == "ldr":
            self.id = module(self.parameter)
    def getmodule(self):
        module_name = self.name
        return self.modules[module_name]
    def resolution(self, period):
        self.period = period
        self.timer = resolution(self.period)
    def report(self):
        data = self.id.reading()
        return data


#   TODO: Relocate sensor alarms to sensor configs, flexible names and pins
M1rgb = RGB(CFG.RGB_WARN_PIN1, CFG.RGB_WARN_PIN2, CFG.RGB_WARN_PIN3)       # RGB sensor-threshold alarm
led_toodark = LED(CFG.LED_WARN1_PIN)                             # LED sensor-threshold alarm

# INITIALIZE SENSORS USING WRAPPER FUNCTION
#   TODO: Easily rename sensors
poll_period = resolution(CFG.POLL_INTERVAL)
if CFG.MOISTURE_S1_ON == True:
    #{name} = sensor('{type}',{serial},{pin(s)})
    #{name}_val = {name}.report()
    #print/onscreen confirmation of name/type
    water = sensor('moisture', CFG.MOISTURE_S1_PIN)
    water.resolution(CFG.POLL_INTERVAL)
    try:
        water_lvl1 = water.report()
        print("Moisture sensor 1 online")
    except:
        print("Check moisture sensor 1")
else:
    water_lvl1 = 0
if CFG.MOISTURE_S2_ON == True:
    water2 = sensor('moisture', CFG.MOISTURE_S2_PIN)
    water2.resolution(CFG.POLL_INTERVAL)
    water_lvl2 = water2.report()
    print("Moisture sensor two online")
else:
    water_lvl2 = 0
if CFG.ULTRASOUND_S1_ON == True:
    ultra = sensor('ultra', (CFG.ULTRASOUND_S1_TRIGGER, CFG.ULTRASOUND_S1_ECHO))
    ultra.resolution(CFG.POLL_INTERVAL)
    ultra_dist = ultra.report()
    print("Ultrasonic range sensor online")
else:
    ultra_dist = 0
if CFG.BMP280_S1_ON == True:
    bmp280 = sensor("thermobaro", (CFG.BMP280_S1_BUS, CFG.BMP280_S1_SCL, CFG.BMP280_S1_SDA, CFG.BMP280_S1_FREQ))
    bmp280.resolution(CFG.POLL_INTERVAL)
    bmp280_temp = bmp280.report()[0]
    bmp280_baro = bmp280.report()[1]
    print("Temperature/Pressure sensor online")
else:
    bmp280_temp = 0
    bmp280_baro = 0
if CFG.LDR_ON == True:
    ldr = sensor("ldr", CFG.LDR_PIN)
    ldr.resolution(CFG.POLL_INTERVAL)
    light_lvl = 0
    print("Light meter online")
else:
    light_lvl = 0

# START LOGGING
log=open(logfile,"w")
#   TODO: Flexible log columns
log.write("Temp (C),Pressure (bar),Moisture Level 1,Moisture Level 2,Light Level,Date,Time")
log.close()
print("Sensor log ready")


# MAIN LOOP
while True:
    sleep(0.1)
    
    # POLL SENSORS AND TRIGGER LEDs/RESPONSES
    if CFG.MOISTURE_S1_ON == True:
        if water.timer.elapsed():
            water_lvl1 = (water.report())
            if water_lvl1 < CFG.MOISTURE_S1_LOW:
                M1rgb.color(M1rgb.r)
            elif water_lvl1 > CFG.MOISTURE_S1_HIGH:
                M1rgb.color(M1rgb.b)
            else:
                M1rgb.color(M1rgb.x)
    if CFG.MOISTURE_S2_ON == True:
        if water2.timer.elapsed():
            water_lvl2 = (water2.report())
    if CFG.ULTRASOUND_S1_ON == True:
        if ultra.timer.elapsed():
            ultra_dist = (ultra.report())
    if CFG.BMP280_S1_ON == True:
        if bmp280.timer.elapsed():
            bmp280_temp = (bmp280.report()[0])
            bmp280_baro = (bmp280.report()[1])
    if CFG.LDR_ON == True:
        if ldr.timer.elapsed():
            light_lvl = (ldr.report())
            if light_lvl < CFG.LDR_LOW:
                led_toodark.state.on()
            else:
                led_toodark.state.off()

    # LOG READINGS
    if poll_period.elapsed():
        CFG.BLINK.pattern(1,.1,.05)
        time = localtime()
        date = f"{time[0]}-{time[1]:02}-{time[2]:02}" 
        hour = f"{time[3]+CFG.TZ:02}:{time[4]:02}"
        timestamp = (date,hour)
        line = f"{bmp280_temp:.02f},{bmp280_baro/100000:.4f},{water_lvl1:.0f},{water_lvl2:.0f},{light_lvl:.0f}"
        log=open(logfile,"a")
        log.write("\n"+line+","+date+","+hour)
        log.close()
        print(line)
        
        
        """TRANSMIT TO WIFI"""
        try:
            if WAN.ip is not "0.0.0.0":
                try:
                    http.serve(connection,'/lib/www/index.html',f"{bmp280_temp:.01f}",f"{bmp280_baro/100000:.2f}",f"{water_lvl1:.0f}",f"{water_lvl2:.0f}",f"{light_lvl:.0f}",date, hour)
                except:
                    pass
        except KeyboardInterrupt:
            machine.reset()
        except:
            pass
        """TRANSMIT TO BT"""
        try:
            serialBluetooth.send(line+'\r\n')
            serialBluetooth.on_write(on_rx)  # Set the callback function for data reception
        except:
            pass
        """REPORT ONSCREEN"""
        try:
            onscreen(f"T:{bmp280_temp:.01f}C P:{bmp280_baro/100000:.2f}b",f"W1:{water_lvl1:.0f}% W2:{water_lvl2:.0f}%",f"L:{light_lvl:.0f}%",hour)
            # todo make $line ^
        except:
            pass

"""
Blink Codes | * = short  -- = long (space = .25s)
=================================================
Board recognized    *
Display enabled     --


Bluetooth selected  * *
Wifi selected       -- --
Bluetooth online    * * *
Wifi online         -- -- --
    

ERROR CODES
Display not found   -- -- -- -- --   -- -- -- -- --

TO DO
=====
TODO: Move Sensor() to lib
TODO: Def wifi/BT connect and reconnect, move to lib
TODO: Separate Sensor_ON and Sensor_DefaultValues so they can be easily switched on/off
TODO: Automatically set list of initialized sensors and only log/pull these, in flexible order
   TODO: Show above list onscreen during startup
TODO: Portable config files
   TODO: Easily rename sensors
   TODO: Relocate sensor alarms to sensor configs, flexible names and pins
   TODO: Config checking
TODO: Improve onscreen() text parameter handling to be more flexible
TODO: Make oled128x32 support arbitrary width/height, set only in config lines
TODO: MERGE led AND blinker
TODO: Device naming
"""