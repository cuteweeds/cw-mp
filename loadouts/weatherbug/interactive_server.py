import machine
import socket
import math
import utime
import network
import time
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("MrHouse2.4","surf ninjas")
 
# rgb led
led=machine.Pin("LED",machine.Pin.OUT)
 
# Wait for connect or fail
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
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
    utime.sleep(2)
    return temperature_Celcius
 
def webpage(value):
    page = open('interactiveindex.html', 'r')
    html = page.read()
    html = html.replace("{value}",value)
    page.close()
    return html
 
def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
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