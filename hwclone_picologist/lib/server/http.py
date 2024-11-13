from machine import Pin, ADC, reset
import socket
from utime import sleep
import network
import time

test_loop = 0

class wifi:
    def __init__(self, ssid, pwd):
        self.ssid=ssid
        self.pwd=pwd
        global wlan
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid,self.pwd)
        wait = 10
        while wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            wait -= 1
            print('waiting for connection...')
            time.sleep(1)
        if wlan.status() == 3:
            print('connected')
            self.ip=wlan.ifconfig()[0]
            print('IP: ', self.ip)
        else:
            print('wifi connection failed')
            self.ip="0.0.0.0"
            #raise RuntimeError('wifi connection failed')

#def webpage(page, bmp280_temp, bmp280_baro, water_lvl1, water_lvl2):
def webpage(page, temperature, pressure, water1, water2, light, date, hour):
    page = str(page)
    temperature = str(temperature)
    pressure = str(pressure)
    water1 = str(water1)
    water2 = str(water2)
    light = str(light)
    date = str(date)
    hour = str(hour)
    page = open(page, 'r')
    html = page.read()
    html = html.replace("{temperature}",temperature)
    html = html.replace("{pressure}",pressure)
    html = html.replace("{water1}",water1)
    html = html.replace("{water2}",water2)
    html = html.replace("{light}",light)
    html = html.replace("{date}",date)
    html = html.replace("{hour}",hour)
    page.close()
    return html

def serve(connection, page, temperature, pressure, water1, water2, light, date, hour):
    global led
    client = connection.accept()[0]
    request = client.recv(8192)
    request = str(request)
    try:
        request = request.split()[1]
    except IndexError:
        pass
    if request == '/led_off?':
        led.off()
    elif request == '/led_on?':
        led.on()  
    html=webpage(page, temperature, pressure, water1, water2, light, date, hour)
    client.send(html)
    client.close()
 
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.settimeout(2)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    print("Online:",connection)
    return(connection)
    
if __name__ == "__main__":
    
    if test_loop == 1:
        
        led=Pin("LED",Pin.OUT)
        wifi("BELL875", "EF31A1FD6F64")
        #WAN = wifi("MrHouse2.4", "surf ninjas")
        print('IP: ', WAN.ip)
        try:
            if WAN.ip is not None:
                connection=open_socket(WAN.ip)
                serve(connection,'/lib/www/interactiveindex.html',1,2,3,4,5)
        except KeyboardInterrupt:
            reset()
            
    if test_loop == 2:
     
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        #wlan.connect("MrHouse2.4","surf ninjas")
        wlan.connect("BELL875", "EF31A1FD6F64")
         
        # rgb led
        led=machine.Pin("LED",machine.Pin.OUT)
         
        # Wait for connect or fail
        wait = 10
        while wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            wait -= 1
            print('waiting for connection...')
            led.toggle()
            time.sleep(1)

        led.off()

        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('wifi connection failed')
        else:
            print('connected')
            ip=wlan.ifconfig()[0]
            print('IP: ', ip)
         
        # Temperature Sensor
        sensor_temp = machine.ADC(4)
        conversion_factor = 3.3 / (65535)
         
        def temperature():
            temperature_value = sensor_temp.read_u16() * conversion_factor 
            temperature_Celcius = 27 - (temperature_value - 0.706)/0.00172169/ 8 
            print(temperature_Celcius)
            sleep(2)
            return temperature_Celcius
         
        def webpage(bmp280_temp,bmp280_baro,water_lvl1,water_lvl2):
            page = open('/lib/www/interactiveindex.html', 'r')
            html = page.read()
            #html = html.replace("{value}",value)
            html = html.replace("{bmp280_temp}", bmp280_temp)
            html = html.replace("{bmp280_baro}", bmp280_baro)
            html = html.replace("{water_lvl1}", water_lvl1)
            html = html.replace("{water_lvl2}", water_lvl2)
            page.close()
            return str(html)
         
        def serve(connection):
            client = connection.accept()[0]
            request = client.recv(8192)
            request = str(request)
            try:
                request = request.split()[1]
            except IndexError:
                pass
            
            print(request)
            
            if request == '/led_off?':
                led.off()
            elif request == '/led_on?':
                led.on()
     
            value='%.2f'%temperature()    
            html=webpage(value)
            client.send(html)
            client.close()
         
        def open_socket(ip):
            # Open a socket
            address = (ip, 80)
            connection = socket.socket()
            connection.bind(address)
            connection.listen(1)
            print(connection)
            return(connection)
        
        try:
            if ip is not None:
                connection=open_socket(ip)
                serve(connection)
        except KeyboardInterrupt:
            machine.reset()