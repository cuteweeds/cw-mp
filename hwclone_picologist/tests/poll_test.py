import time

class event:
    starttime = time.time()
    
    def __init__(self, name, period):
        self.name = name
        self.period = period
        
    def poll(self):
        delta = time.time() - self.starttime
        if delta > self.period:
            #reset timer
            self.starttime = time.time()
            #take action
            print(self.name)
            
# initialize shouts
euch = event("euch",0.3)
yow = event("  yow",0.21)
eep = event("    eep",0.57)

# Poll loop
starttime = time.time()
while True:
    time.sleep(0.01)
    seconds = round(time.time() - starttime,1)
    euch.poll()
    yow.poll()
    eep.poll()