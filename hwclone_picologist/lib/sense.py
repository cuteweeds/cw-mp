from utime import sleep, ticks_ms

class resolution:
    starttime = ticks_ms()
    
    def __init__(self, period):
        # self.name = name
        self.period = period
        
    def elapsed(self):
        delta = ticks_ms() - self.starttime
        if delta > self.period:
            self.starttime = ticks_ms()
            return True
            
def react(string):
    print(string)

# Poll loop
if __name__ == "__main__":
    # initialize triggers
    euch = resolution(3000)
    yow = resolution(600)
    eep = resolution(800)

    starttime = ticks_ms()
    while True:
        sleep(0.1)
        seconds = round(ticks_ms() - starttime,1)
        if euch.elapsed(): react("euch")
        if yow.elapsed(): react("yow")
        if eep.elapsed(): react("eep")