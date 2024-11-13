import base64

password={
	"MrHouse2.4" 	: 	"c3VyZiBuaW5qYXM=",
	"BELL875" 		: 	"RUYzMUExRkQ2RjY0"
	}

networks = [
    ("MrHouse2.4","bssid", "channel", "RSSI", "security", "hidden"),
	("BELL875","agsdf", "nfg", "aewr", "vafdvasd", "sdaf"),
	("eh","uh","oh","ee","oo","ah"), 	# no match, no problem
	("wtf","s453",29)					# bad network shouldn't cause error
	]

for key in password:
 for net in networks:
  if key == net[0]:
   SSID = key
   PASSWORD = base64.b64decode(password[key].encode("ascii")).decode("ascii")
   print(PASSWORD)