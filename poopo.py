from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# Initialize I2C
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=200000)

# Scan for devices
devices = i2c.scan()
if not devices:
    print("No I2C devices found. Check connections.")
else:
    print(f"I2C devices found: {devices}")

# If address is detected, proceed to initialize OLED
if 0x3C in devices:  # Replace 0x3C with your OLED's I2C address if different
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.text("BLANK", 32, 20)
    oled.show()
else:
    print("SSD1306 not detected. Check wiring or address.")
