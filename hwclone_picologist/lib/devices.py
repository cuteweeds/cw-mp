def bluetooth(boolean):
    global btMode
    """IMPORT BLUETOOTH AND WIFI"""
    if boolean == True:
        import bluetooth
        from ble_simple_peripheral import BLESimplePeripheral
        ble = bluetooth.BLE()
        serialBluetooth = BLESimplePeripheral(ble)
    else:
        pass
    return serialBluetooth
    # TODO: auto reconnect BT
    # TODO: Device naming

def wifi(boolean, SSID, PASSWORD):
    global wifiMode
    if boolean == True:
        import server.http as http
        wifiMode="Wifi"
        print("Starting Wifi")
        WAN = http.wifi(SSID, PASSWORD)
        if WAN.ip == "0.0.0.0":
            WIFI_ON=False
            print("No IP: ",WAN.ip)
        # TODO: auto reconnect Wifi
    else:
        wifiMode=""
    return WAN

if __name__=="__main__":
    WAN = wifi(True,"MrHouse2.4","surf ninjas")
    #connection = WAN.connection()
    print(WAN)
    ##while True:
    ##    WAN.serve(WAN.connection,'/lib/www/index.html',1,2,3,4,5,6,7)
    ##    sleep(1)
"""INITIALIZE WIFI

if CFG.WIFI_ON==True:
    
        print("Can't sync time. Using device default time")
        try:
            onscreen("Can't sync time.","Using default.","","")
            CFG.TZ=0
        except:
            pass
    else:
        connection=session.open_socket(WAN.ip)
        oled.display.text("BT: On Wifi: On",0,24)
        oled.display.show()
        sleep(.75)
        onscreen("Online:",WAN.ip,"","")
"""


"""
if CFG.BLUETOOTH_ON == True:
    
    oled.display.text("BT: On Wifi:   ",0,24)
    oled.display.show()
    print("Bluetooth on")
    CFG.BLINK.pattern(3,.25,.25)
    # DEFINE BLUETOOTH TRIGGERS
    def on_rx(data):
        print("Data received: ", data)
        global BOARD_LED_STATE                    # Variable(s) to be set by any incoming BT instructions
        if data == b'flick\r\n':                  # Setup keyword trigger(s) for incoming BT instructions
            led.value(not BOARD_LED_STATE)   
            BOARD_LED_STATE = 1 - BOARD_LED_STATE
            """