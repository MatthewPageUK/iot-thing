#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  Additional functions and helpers for the test scripts.
#  Mostly formatting and non-essential things.
#
#  log(text1, text2)    Outputs log text
#  flash_led(led)       Flashes the LED
#  splash(title)        Displays a splash screen on the LCD
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from sys import exit
from time import sleep

def log(text1, text2 = None):
    """Write some text out to the display

    Parameters
    ----------
    text1
        The text to print out
    text2
        Optional text to show in --[ here ]--
    """
    if text2 is not None:
        print("| {t1:<25} --[ {t2:<16} ]--".format(
            t1 = str(text1),
            t2 = str(text2)))
    else:
        print("| {t1}".format(t1 = str(text1)))

def flash_led(led: Pin):
    """Flash the LED

    Parameters
    ----------
    led : Pin
        The LED Pin to use
    """
    try:
        led.off()
        for i in range(6):
            led.toggle()
            sleep(0.1)

    except AttributeError as err:
        log("Failed to control LED", err)
        exit(0)

def splash(title: str):
    """Show a splash screen

    Parameters
    ----------
    title : str
        The splash screen title
    """
    print(" __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___ ")
    print("(  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)")
    print(" )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.")
    print("(_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/")
    print("________________________________________________________________")
    print("|\n| {t}\n|".format(t = title))

