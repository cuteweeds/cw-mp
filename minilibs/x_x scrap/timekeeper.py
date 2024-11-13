import ntpcfg as CFG
import checkntp
import utime
from machine import RTC

timezone_hours = CFG.TZ

rtc = RTC()
rtc.datetime(checkntp.setclock(timezone_hours))
print(utime.localtime())