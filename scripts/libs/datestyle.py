from utime import localtime

class Timestamp:
    def __init__(self):
        t=localtime()
        Y=t[0]
        M=t[1]
        D=t[2]
        h=t[3]
        m=t[4]
        s=t[5]
    
    def YYYYMMDD(self,s):
        s=str(s)
        format="{:4d}{}{:02d}{}{:02d}".format(Y,s,M,s,D)
    
    def style(self,style,s):
        s=str(s)
        fY=s.find("Y")
        
    def datestyle(self,instring,sep):
        units="YMDhms"
        count = {}
        places = []
        instring = str(instring)
        sep = str(sep)
        
        # Get count of each valid unit of time in format specifier input as a dictionary to clobber duplicates
        for n in units:
            count.update( {n:instring.count(n)} )
            
        # Convert dictionary to a list of the values
        for key, value in dict.items(count):
            places.append(str(value))
        
        # Calculate format specifier output
        Y = ("\{\:" + places[0] + "d\}" + sep if int(places[1])>0 else "") if int(places[0])>0 else ""
        M = ("\{\:" + places[1] + "d\}" + sep if int(places[1])>0 else "") if int(places[1])>0 else ""
        D = ("\{\:" + places[2] + "d\}" + sep if int(places[3])>0 else "") if int(places[2])>0 else ""
        h = ("\{\:" + places[3] + "d\}" + sep if int(places[1])>0 else "") if int(places[3])>0 else ""
        m = ("\{\:" + places[4] + "d\}" + sep if int(places[1])>0 else "") if int(places[4])>0 else ""
        s = ("\{\:" + places[5] + "d\}") if int(places[5])>0 else ""
        self.datestyle=Y+M+D+h+m+s
        return self.datestyle
        
now=Timestamp()
form=now.datestyle("YYYYMMMDDh","-")
print(form)