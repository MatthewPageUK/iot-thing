#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  LCD setup and test.
#
#  Blinks the display backlight twice and animates some text on the
#  screen. If you don't see anything try adjusting the contrast of
#  your display.
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from machine import Pin, I2C
from time import sleep
try:
    from pico_i2c_lcd import I2cLcd
except ImportError:
    print("\nPlease save 'pico_i2c_lcd.py' and 'lcd_api.py' files to your Thing before running the test\n\n")
    exit(0)
try:
    from thing_test import log, flash_led, splash
except ImportError:
    print("\nPlease save 'thing_test.py' file to your Thing before running the test\n\n")
    exit(0)

##############################################################################
# Test settings
##############################################################################

# LCD I2C Channel
LCD_ID = 1

# Pins the LCD is connected to
LCD_PIN_SDA = 6
LCD_PIN_SCL = 7

# LCD Settings
LCD_ADDR = 0x3F
LCD_FREQ = 100000
LCD_COLUMNS = 16
LCD_LINES = 2

# Title text to show on the display
TITLE = "Matt's Thing"

##############################################################################
# Test setup
##############################################################################

# Create the I2C interface
lcdI2c = I2C(
    id = LCD_ID,
    sda = Pin(LCD_PIN_SDA),
    scl = Pin(LCD_PIN_SCL),
    freq = LCD_FREQ)

# Create the LCD instance with the I2C interface
lcd = I2cLcd(
    i2c = lcdI2c,
    i2c_addr = LCD_ADDR,
    num_lines = LCD_LINES,
    num_columns = LCD_COLUMNS)

# Main program
splash("LCD test")

##############################################################################
# Run the test
##############################################################################
while True:

    log("Test running - look at your LCD display not here...")
    lcd.clear()

    # Flash the backlight
    for i in range(2):
        lcd.backlight_off()
        sleep(0.5)
        lcd.backlight_on()
        sleep(0.5)

    # Animate some text
    for repeat in range(5):
        for position in range(LCD_COLUMNS - len(TITLE)):
            lcd.clear()
            lcd.putstr(" " * position + TITLE)
            sleep(0.5)
        for position in range(LCD_COLUMNS - len(TITLE), 0, -1):
            lcd.clear()
            lcd.putstr(" " * position + TITLE)
            sleep(0.5)

    lcd.clear()
    lcd.putstr(TITLE)
    sleep(2)
