"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import usys
import ustruct as struct
import utime
from machine import Pin, SPI
from NRF24L01.nrf24l01 import NRF24L01
from micropython import const

# peripheral pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)
# peripheral pauses an additional _peripheral_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) controller time to get into receive mode. The
# controller may be a slow device. Value tested with Pyboard, ESP32 and ESP8266.
_peripheral_SEND_DELAY = const(10)

if usys.platform == "pyboard":
    cfg = {"spi": 2, "cipo": "Y7", "copi": "Y8", "sck": "Y6", "csn": "Y5", "ce": "Y4"}
elif usys.platform == "esp8266":  # Hardware SPI
    cfg = {"spi": 1, "cipo": 12, "copi": 13, "sck": 14, "csn": 4, "ce": 5}
elif usys.platform == "esp32":  # Software SPI
    cfg = {"spi": -1, "cipo": 32, "copi": 33, "sck": 25, "csn": 26, "ce": 27}
elif usys.platform == "rp2":
    cfg = {"spi": 0, "cipo": 16, "copi": 19, "sck": 18, "csn": 17, "ce": 20}
else:
    raise ValueError("Unsupported platform {}".format(usys.platform))

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")


def controller():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    if cfg["spi"] == -1:
        spi = SPI(-1, sck=Pin(cfg["sck"]), copi=Pin(cfg["copi"]), cipo=Pin(cfg["cipo"]))
        nrf = NRF24L01(spi, csn, ce, payload_size=8)
    else:
        nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, payload_size=8)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    num_needed = 16
    num_successes = 0
    num_failures = 0
    led_state = 0

    print("NRF24L01 controller mode, sending %d packets..." % num_needed)

    while num_successes < num_needed and num_failures < num_needed:
        # stop listening and send packet
        nrf.stop_listening()
        millis = utime.ticks_ms()
        led_state = max(1, (led_state << 1) & 0x0F)
        print("sending:", millis, led_state)
        try:
            nrf.send(struct.pack("ii", millis, led_state))
        except OSError:
            pass

        # start listening again
        nrf.start_listening()

        # wait for response, with 250ms timeout
        start_time = utime.ticks_ms()
        timeout = False
        while not nrf.any() and not timeout:
            if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
                timeout = True

        if timeout:
            print("failed, response timed out")
            num_failures += 1

        else:
            # recv packet
            (got_millis,) = struct.unpack("i", nrf.recv())

            # print response and round-trip delay
            print(
                "got response:",
                got_millis,
                "(delay",
                utime.ticks_diff(utime.ticks_ms(), got_millis),
                "ms)",
            )
            num_successes += 1

        # delay then loop
        utime.sleep_ms(250)

    print("controller finished sending; successes=%d, failures=%d" % (num_successes, num_failures))


def peripheral():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    if cfg["spi"] == -1:
        spi = SPI(-1, sck=Pin(cfg["sck"]), copi=Pin(cfg["copi"]), cipo=Pin(cfg["cipo"]))
        nrf = NRF24L01(spi, csn, ce, payload_size=8)
    else:
        nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, payload_size=8)

    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    print("NRF24L01 peripheral mode, waiting for packets... (ctrl-C to stop)")

    while True:
        if nrf.any():
            while nrf.any():
                buf = nrf.recv()
                millis, led_state = struct.unpack("ii", buf)
                print("received:", millis, led_state)
                for led in leds:
                    if led_state & 1:
                        led.on()
                    else:
                        led.off()
                    led_state >>= 1
                utime.sleep_ms(_RX_POLL_DELAY)

            # Give controller time to get into receive mode.
            utime.sleep_ms(_peripheral_SEND_DELAY)
            nrf.stop_listening()
            try:
                nrf.send(struct.pack("i", millis))
            except OSError:
                pass
            print("sent response")
            nrf.start_listening()


try:
    import pyb

    leds = [pyb.LED(i + 1) for i in range(4)]
except:
    leds = []

print("NRF24L01 test module loaded")
print("NRF24L01 pinout for test:")
print("    CE on", cfg["ce"])
print("    CSN on", cfg["csn"])
print("    SCK on", cfg["sck"])
print("    cipo on", cfg["cipo"])
print("    copi on", cfg["copi"])
print("run nrf24l01test.peripheral() on peripheral, then nrf24l01test.controller() on controller")
