#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  Button setup test.
#
#  Waits for a button press and displays a count of how many times
#  the button has been pressed. If nothing has happened for
#  WAITIN_PERIOD intervals displays a waiting message.
#
#  If your button doesn't respond, please check it is not a broken, had a few that
#  either don't work or stop working after a few clicks.
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from time import sleep
from machine import Pin
try:
    from thing_test import log, flash_led, splash
except ImportError:
    print("\nPlease save 'thing_test.py' file to your Thing before running the test\n\n")
    exit(0)

##############################################################################
# Test settings
##############################################################################

# The pin the button is connected to
BUTTON_PIN = 14

# Intervals to wait for a button press
WAIT_PERIOD = 200000

##############################################################################
# Test setup
##############################################################################

# Setup the LED Pin
led = Pin('LED', Pin.OUT)

# Setup the Button Pin
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

# Count how many times we press it
count = 0

# Timer to show a waiting message
waiting = WAIT_PERIOD

# Main program
splash("Button setup test - please press my button...")

##############################################################################
# Run the test
##############################################################################
while True:

    # If the button has been pressed
    if button.value():
        count += 1
        log("You pressed my button {c} times.".format(c = count))
        waiting = WAIT_PERIOD
        sleep(0.5)

    # Waiting prompt
    if waiting == 0:
        log("I'm waiting...")
        waiting = WAIT_PERIOD
    else:
        waiting -= 1