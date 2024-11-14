try:
    SPI1_SCK    = 10
    SPI1_COPI   = 11
    SPI1_A0     = 8
    SPI1_RESET  = 12
    SPI1_CS     = 9
    tft_SCK = SPI1_SCK
    tft_SDA = SPI1_COPI
    tft_A0_ = SPI1_A0
    tft_RES = SPI1_RESET
    tft_CS_ = SPI1_CS
    tft_BL = 13
except:
    raise Exception("Set SPI pins in cfg to attach devices")
