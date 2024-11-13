import wifi_connect 
import ntptime
from utime import localtime
from machine import RTC

def setclock(timezone_hours):
    rtc = RTC()
    ntptime.settime()
    timezone_seconds = timezone_hours * 3600
    time_seconds = ntptime.time()
    time_seconds = int(time_seconds + timezone_seconds)
    
    (year, month, day, hours, minutes, seconds, weekday, yearday) = localtime(time_seconds)
    return [year, month, day, weekday, hours, minutes, seconds, 0]

if __name__ == "__main__":
    rtc = RTC()
    TZ = -5
    tm = checkntp(TZ)
    print(tm)