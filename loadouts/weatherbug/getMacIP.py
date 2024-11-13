import network
import time
import ubinascii
#import machine
import gc

'''
get_mac_and_ip.py

This script gets pico w's mac number and ip address from your wlan.
Those are needed when configuring wlan or connecting pico w to internet or to local network.

And later, in my case, I needed pico's ip and port number to
configure my firewall, so that it allows network traffic happen
between pico's sw and other device's sw. 

You can use also run arp -a on command line to get network
ip and mac numbers.
'''

ssid = "MrHouse2.4"
pw = "surf ninjas"
connected = False

gc.collect()
time.sleep(2)

# on-board led is not recommended to use but ...
# left here in comments if someone wants to use it
# led = machine.Pin('LED', machine.Pin.OUT)
# led.on() and led.off()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(ssid, pw)

timeout = 10
while timeout > 0:
    if wlan.status() >= 3:
        connected = True
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

time.sleep(2)

if connected == True:

    wlan_status = wlan.status()
    print(wlan_status)
    
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print(mac)

    ip = wlan.ifconfig()[0]
    print(ip)

    wlan_status = wlan.status()
    print(wlan_status)
else:
    print("Failed to get mac and ip")
    
if wlan != None:
    wlan.disconnect()
    print("wlan diconnected!")