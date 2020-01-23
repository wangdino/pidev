import smbus


ADC_ADDR = 0x48
CHN_ADDR = {
    'AIN0' : 0x40,
    'AIN1' : 0x41,
    'AIN2' : 0xA2,
    'AIN3' : 0xA3
}


class Signal(object):

    def __init__(self, channel):
        self.channel_address = CHN_ADDR[channel]
        self.bus = smbus.SMBus(1)

    def measure(self):
        self.bus.write_byte(ADC_ADDR, self.channel_address)
        raw = self.bus.read_byte(ADC_ADDR)
        return raw * 3.3 / 255
