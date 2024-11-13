import network
import socket
import time
import struct
from machine import Pin, RTC

def set_time():
    NTP_DELTA = 2208988800
    NTP_HOST= "pool.ntp.org"
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    try:
        addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        t = val - NTP_DELTA    
        tm = time.gmtime(t)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3] - 4, tm[4], tm[5], 0))
        START_TIME = RTC().datetime()
        ntplogfile = str(f"logs/ntplog.csv")
        ntplog=open(ntplogfile,"a")
        ntplog.write(str(START_TIME)+'\n')
        ntplog.close()
    except:
        START_TIME = str(RTC().datetime())
        ntplogfile = str(f"logs/ntplog.csv")
        ntplog=open(ntplogfile,"a")
        ntplog.write("Couldn't connect to NTP server"+'\n')
        ntplog.close()
    return START_TIME
        
if __name__ == "__main__":
    ssid="MrHouse2.4"
    password="surf ninjas"
    led=Pin("LED",Pin.OUT)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

    led.on()
    set_time()
    print(time.localtime())
    led.off()