# DS3231 RTC
# Integrated temperature compensated crystal oscillator (TCXO)

import smbus
import datetime

ADDRESS = 0x68
REGISTER = 0x00
BUS = smbus.SMBus(1)

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class RTC:

    def __init__(self):
        self.addr = ADDRESS
        self.reg = REGISTER
        self.bus = BUS
        self.now = datetime.datetime.now()
        self.weekday = datetime.datetime.now().isoweekday()

    def set_datetime(self, user_input=None):
        if user_input is None:
            sys_time = 0  # dummy
            self.bus.write_i2c_block_data(self.addr, self.reg, sys_time)
        else:
            try:
                user_time = 0  # dummy
                self.bus.write_i2c_block_data(self.addr, self.reg, user_time)
            except:
                return 200
        return 99

    def get_datetime(self):
        curr_time = self.bus.read_i2c_block_data(self.addr, self.reg, 7)
        ss = curr_time[0] & 0x7F
        mm = curr_time[1] & 0x7F
        hh = curr_time[2] & 0x3F
        weekday = curr_time[3] & 0x07
        day = curr_time[4] & 0x3F
        month = curr_time[5] & 0x1F
        year = curr_time[6]
        curr_time_str = '-'.join([year, month, day])\
                        + ' ' + WEEKDAYS[weekday-1] + ' '\
                        + ':'.join([hh, mm, ss])
