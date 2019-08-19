# DS3231 RTC
# Integrated temperature compensated crystal oscillator (TCXO)

import smbus
import datetime

ADDRESS = 0x68
REGISTER = 0x00
BUS = smbus.SMBus(1)

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class Clock:

    def __init__(self):
        self.addr = ADDRESS
        self.reg = REGISTER
        self.bus = BUS
        self.now = datetime.datetime.now()
        self.weekday = datetime.datetime.now().isoweekday()

    def rtc_encode(self, sys_time):
        def conv(n):
            hex_str = hex(int((n - n % 10) / 10 * 16) + n % 10)
            return int(hex_str, 16)
        ss = conv(sys_time.second)
        mm = conv(sys_time.minute)
        hh = conv(sys_time.hour)
        day = conv(sys_time.day)
        month = conv(sys_time.month)
        year = conv(sys_time.year - 2000)
        weekday = sys_time.isoweekday()
        return [ss, mm, hh, weekday, day, month, year]

    def rtc_decode(self, raw_time):
        ss = int('%02x' % (raw_time[0] & 0x7F))
        mm = int('%02x' % (raw_time[1] & 0x7F))
        hh = int('%02x' % (raw_time[2] & 0x3F))
        # weekday = int((raw_time[3] & 0x07)) - 1
        day = int('%02x' % (raw_time[4] & 0x3F))
        month = int('%02x' % (raw_time[5] & 0x1F))
        year = int('%02x' % (raw_time[6] & 0xFF)) + 2000
        sys_time = datetime.datetime(year, month, day, hh, mm, ss)
        return sys_time

    def get_sys_time(self):
        sys_time = datetime.datetime.now()
        return sys_time

    def construct_sys_time(self, user_input):
        # user_input must be an array in form of:
        # [year, month, day, hour, minute, second]
        year = user_input[0]
        month = user_input[1]
        day = user_input[2]
        hh = user_input[3]
        mm = user_input[4]
        ss = user_input[5]
        return datetime.datetime(year, month, day, hh, mm, ss)

    def set_datetime(self, user_input=None):
        if user_input is None:
            set_time = self.get_sys_time()
            self.bus.write_i2c_block_data(self.addr, self.reg, set_time)
        else:
            set_time = self.construct_sys_time(user_input)
            self.bus.write_i2c_block_data(self.addr, self.reg, set_time)
        return

    def get_datetime(self, output_obj=True):
        curr_time_raw = self.bus.read_i2c_block_data(self.addr, self.reg, 7)
        curr_time = self.rtc_decode(curr_time_raw)
        if output_obj is True:
            return curr_time
        else:
            weekday = WEEKDAYS[curr_time.weekday()]
            curr_time_str = curr_time.isoformat(' ') + ' ' + weekday
            return curr_time_str
