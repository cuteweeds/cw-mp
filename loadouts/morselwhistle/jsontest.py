from machine import Pin
import json
led = Pin(28,Pin.OUT)

def preplist(lst):
    res_list = []
    for i in range(len(lst)):
        res_list.append((lst[i]["key"], lst[i]["val"]))
        print(lst[i]["key"])
    return(res_list)

def prepdict(lst):
    print("building dictionary…")
    print()
    dict = {}
    for i in range(len(lst)):
        dict[lst[i]["key"]] = lst[i]["val"]
        #led.toggle()
        #machine.lightsleep(20)
    led.off()
    return dict

#data = '[{"key" : "a", "value": "01"}, { "key" : "A", "value" : "01"}, { "key" : "b", "value" : "11" }, { "key" : "B" , "value" : "11" }]'
#testdict = json.loads(data)
#print(dict[0]["value"])
#print(dir(testdict))
#print(dir(re))
#print(len(testdict))
    
with open("morse.json","r") as extdata:
    jsondata = json.load(extdata)
    
print("External data is ",jsondata.__class__)
print("JSON element count is ",len(jsondata))
print()
#print("ALL KEY-VALUE PAIRS")

#for i in range(len(jsondata)):
#    print(jsondata[i]["key"] + ": " + jsondata[i]["val"])
    #led.toggle()
    #machine.lightsleep(20)
#led.off()
print('*******')

#json3 = '[{"a":"01","A":"01","b":"02","B":"02","c":"03","C":"03"}]'
#jsondict = json.loads(json3)
#print(jsondict)

#dict = makedict(jsondata)
#print(type(dict))


#realdict = {"morse a" : "01", "morse b": "02"}
#print(realdict.__class__)
#code = realdict.get("morse b")
#print(code)

dictionary = prepdict(jsondata)
print(dir(dictionary))
print(type(dictionary)," Length: ",len(dictionary))
target="o"
a = dictionary.get(target)
print(a)