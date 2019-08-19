import pidev.RTC.RTC

rtc = pidev.RTC.RTC.Clock()
print(rtc.get_datetime())
