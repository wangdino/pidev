import smbus
import datetime

# DS3231 RTC
# Integrated temperature compensated crystal oscillator (TCXO)
ADDRESS = 0x68
REGISTER = 0x00
BYTES = 7
BUS = smbus.SMBus(1)
# Timekeeping Registers
YEAR_MASK = 0xFF
MONTH_MASK = 0x1F
DAY_MASK = 0x3F
HOUR_MASK = 0x3F
MINUTE_MASK = 0x7F
SECOND_MASK = 0x7F
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class Clock:

    def __init__(self):
        self.addr = ADDRESS
        self.reg = REGISTER
        self.bytes = BYTES
        self.bus = BUS

    def set_datetime(self, user_input=None):
        if user_input is None:
            set_time = rtc_encode(get_sys_time())
            self.bus.write_i2c_block_data(self.addr, self.reg, set_time)
        else:
            set_time = rtc_encode(construct_sys_time(user_input))
            self.bus.write_i2c_block_data(self.addr, self.reg, set_time)
        return

    def get_datetime(self, output_obj=True):
        curr_time_raw = self.bus.read_i2c_block_data(self.addr, self.reg, self.bytes)
        curr_time = rtc_decode(curr_time_raw)
        if output_obj is True:
            return curr_time
        else:
            weekday = WEEKDAYS[curr_time.weekday()]
            curr_time_str = curr_time.isoformat(' ') + ' ' + weekday
            return curr_time_str


# Static Functions
def conv(n):
    hex_str = hex(int((n - n % 10) / 10 * 16) + n % 10)
    return int(hex_str, 16)


def rtc_encode(sys_time):
    ss = conv(sys_time.second)
    mm = conv(sys_time.minute)
    hh = conv(sys_time.hour)
    day = conv(sys_time.day)
    month = conv(sys_time.month)
    year = conv(sys_time.year - 2000)
    weekday = sys_time.isoweekday()
    return [ss, mm, hh, weekday, day, month, year]


def rtc_decode(raw_time):
    ss = int('%02x' % (raw_time[0] & SECOND_MASK))
    mm = int('%02x' % (raw_time[1] & MINUTE_MASK))
    hh = int('%02x' % (raw_time[2] & HOUR_MASK))
    day = int('%02x' % (raw_time[4] & DAY_MASK))
    month = int('%02x' % (raw_time[5] & MONTH_MASK))
    year = int('%02x' % (raw_time[6] & YEAR_MASK)) + 2000
    sys_time = datetime.datetime(year, month, day, hh, mm, ss)
    return sys_time


def get_sys_time():
    sys_time = datetime.datetime.now()
    return sys_time


def construct_sys_time(user_input):
    # user_input must be an array in form of:
    # [year, month, day, hour, minute, second]
    year = user_input[0]
    month = user_input[1]
    day = user_input[2]
    hh = user_input[3]
    mm = user_input[4]
    ss = user_input[5]
    return datetime.datetime(year, month, day, hh, mm, ss)

