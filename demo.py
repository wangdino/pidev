import time


def test_clock():
    import pidev.Clock
    clk = pidev.Clock.DS3231()
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
    return


def test_screen():
    import pidev.Screen
    import spidev
    from PIL import Image, ImageDraw, ImageFont
    oled = pidev.Screen.SSD1306(19, 16, spidev.SpiDev(0, 0))
    oled.begin()
    oled.clear()
    oled.display()
    image = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 127, 15), outline=1, fill=0)
    draw.rectangle((0, 16, 127, 63), outline=1, fill=0)
    font = ImageFont.load_default()
    draw.text((2, 2), 'Hello', font=font, fill=255)
    draw.text((2, 22), 'World!', font=font, fill=255)
    oled.image(image)
    oled.display()
    return


def adc_show():
    import spidev
    import pidev.Screen
    import pidev.ADC
    from PIL import Image, ImageDraw, ImageFont
    oled = pidev.Screen.SSD1306(19, 16, spidev.SpiDev(0, 0))
    oled.begin()
    oled.clear()
    oled.display()
    image = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    signal = pidev.ADC.Signal('AIN0')
    while True:
        value = signal.measure()
        draw.text((2, 18), '{:.3f}'.format(value), font=font, fill=255)
        oled.image(image)
        oled.display()
        time.sleep(1)


def main():
    adc_show()
    return


if __name__ == "__main__":
    main()
