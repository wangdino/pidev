import time
import pidev.RTC.RTC

rtc = pidev.RTC.RTC.Clock()

print('Setting time to 2013-02-15 16:30:59')
rtc.set_datetime([2013, 2, 15, 16, 30, 59])
print('Checking time:')
i = 0
for i in range(5):
    print(rtc.get_datetime(output_obj=False))
    i += 1
