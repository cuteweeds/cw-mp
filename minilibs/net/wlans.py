import network
import sys
import json
from utime import sleep_ms   

def connect(file):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    
    # Import JSON network credentials
    lst = get_networks(file)
    for n in range(len(lst)):
        ssid = lst[n]['ssid']
        pwd = lst[n]['pwd']
        print(ssid, pwd)
        timeout = 10
        wifi.connect(ssid, pwd)
        for i in range(timeout):
            while i < timeout:
                if wifi.status() < 0 or wifi.status() >= 3:
                    break
            blink.pattern(1,.15,.15)
        if wifi.status() != 3:
            wifi.active(False)
            sleep_ms(250)
        else:
            ip = wifi.ifconfig()[0]
            print("IP: ", ip, wifi.status())
            blink.pattern(4,.05,.05)
            break
    return wifi

def get_networks(file):
    with open(file, 'r') as data:
        raw = json.load(data)
        lst = raw["credentials"]
    return lst

def prepdict(lst):             
    rdict = {}
    for i in range(len(lst)):
        rdict[lst[i]['ssid']] = lst[i]['pwd']
    print(rdict)
    return rdict

if __name__ == "__main__":
    from board.blinker import blinker
    wifi = connect('netlist.json')