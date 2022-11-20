#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  BME280 Sensor test and setup.
#
#  Reads data from the sensor and displays a formatted string.
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from machine import Pin, I2C
from time import sleep
try:
    import bme280
except ImportError:
    print("\nPlease save 'bme280.py' file to your Thing before running the test\n\n")
    exit(0)
try:
    from thing_test import log, flash_led, splash
except ImportError:
    print("\nPlease save 'thing_test.py' file to your Thing before running the test\n\n")
    exit(0)

##############################################################################
# Test settings
##############################################################################

# BME I2C Channel
BME280_ID = 0

# Pins the BME is connected to
BME280_PIN_SDA = 0
BME280_PIN_SCL = 1

# BME frequency
BME280_FREQ = 400000

def formatData(sensor: bme280):
    """Return the data from the sensor as a string

    Parameters
    ----------
    sensor : bme280
        The sensor to read

    Returns
    -------
    str
        The data formatted in a string
    """
    temperature = sensor.values[0]
    pressure = sensor.values[1]
    humidity = sensor.values[2]

    text = "Temperature : {t}  Pressure : {p}  Humidity : {h}"
    return text.format(t = temperature, p = pressure, h = humidity)

##############################################################################
# Test setup
##############################################################################

# Setup the LED Pin
led = Pin('LED', Pin.OUT)

# Setup the I2C interface on the BME pins
bmeI2c = I2C(
    id = BME280_ID,
    sda = Pin(BME280_PIN_SDA),
    scl = Pin(BME280_PIN_SCL),
    freq = BME280_FREQ)

# Create the BME instance with the I2C interface
bmeSensor = bme280.BME280(i2c = bmeI2c)

# Main program
splash("BME280 Sensor test")

##############################################################################
# Run the test
##############################################################################
while True:

    log("Reading sensor data", formatData(bmeSensor))
    flash_led(led)
    sleep(1)
