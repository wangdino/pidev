import time
import pidev.RTC.RTC as rtc

clk = rtc.DS3231()

print('Setting time to 2013-02-15 16:30:59 ...')
clk.set_datetime(user_input=[2013, 2, 15, 16, 30, 59])
print('Checking time:')
i = 0
for i in range(5):
    print(clk.get_datetime(output_obj=False))
    i += 1
    time.sleep(1)
print('Setting time to current system time ...')
clk.set_datetime()
print('Checking time:')
i = 0
for i in range(5):
    print(clk.get_datetime(output_obj=False))
    i += 1
    time.sleep(1)
