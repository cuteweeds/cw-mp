import server.http as session
from ntp import set_time
from utime import localtime
from machine import RTC

SSID="BELL875"
#SSID="MrHouse2.4"
PASSWORD="EF31A1FD6F64"
#PASSWORD="surf ninjas"

print("network libraries")
WAN = session.wifi(SSID, PASSWORD)
try:
    print('IP: ', WAN.ip)
    
    print("checking NTP")
    set_time()
    print("local time: ",f"{localtime()[0]}-{localtime()[1]}-{localtime()[2]:02f} {localtime()[3]}:{localtime()[4]:02f}:{localtime()[5]:02f}")
    
    
except:
    pass
print("over to you")
time=RTC().datetime()
print("start_time read as: ",time)
date = f"{time[0]}{time[1]:02}{time[2]:02}" 
hour = f"{time[4]}:{time[5]:02}"

timestamp = (date,hour)
logfile = "logs/"+timestamp[0]+"-"+timestamp[1]+".csv"

print("Timestamp: ",timestamp)
print("Logfile name: ",logfile)