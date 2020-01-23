import smbus


DAC_ADDR = 0x48
DAC_CMMD = 0x40
bus = smbus.SMBus(1)
