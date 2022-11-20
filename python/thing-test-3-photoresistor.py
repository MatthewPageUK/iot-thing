#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  Photoresistor test and read-out
#  Higher values darker, lower values brighter
#
#  Shine a bright torch on your sensor and then cover it completely
#  to calibrate the percentage value.
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from machine import ADC
from time import sleep
try:
    from thing_test import log, flash_led, splash
except ImportError:
    print("\nPlease save 'thing_test.py' file to your Thing before running the test\n\n")
    exit(0)

##############################################################################
# Test settings
##############################################################################

# The pin the photoresistor is connected to
PHOTORESISTOR_PIN = 27

##############################################################################
# Test setup
##############################################################################

# Setup the photoresistor with analogue to digital converter
photoResistor = ADC(PHOTORESISTOR_PIN)

# Main program
splash("Testing photoresitor output")

# Remember max and min values, useful for calibrating code
maxLight = None
minLight = None

##############################################################################
# Run the test
##############################################################################
while True:

    # Read the value
    light = photoResistor.read_u16()
    
    # Remember max and min
    if maxLight is None or maxLight < light:
        maxLight = light
    if minLight is None or minLight > light:
        minLight = light
       
    # Calculate the percent based on max and min
    try:
        percent = 100 - ( ( 100 / ( maxLight - minLight ) ) * ( light - minLight ) )
    except ZeroDivisionError:
        percent = -1
        
    log("Reading light value",
        "{l} ({p:.1f}%)   Max : {mx}  Min : {mn}".format(
            l = light,
            p = percent,
            mx = maxLight,
            mn = minLight))
    
    sleep(1)
