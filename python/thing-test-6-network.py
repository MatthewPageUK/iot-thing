#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  Network setup and test.
#
#  xxxxx
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from sys import exit
from time import sleep
from machine import Pin
import network
import socket
import urequests
try:
    from thing_test import log, flash_led, splash
except ImportError:
    print("\nPlease save 'thing_test.py' file to your Thing before running the test\n\n")
    exit(0)

##############################################################################
# Test settings
##############################################################################

# WiFi Settings
WIFI_SSID = "mattnet"
WIFI_PASSWORD = "letmeout"

TEST_URL = "http://www.example.com"

##############################################################################
# Test setup
##############################################################################

# Setup the LED Pin
led = Pin('LED', Pin.OUT)

# Maximum time to wait for a network connection
wifiMaxWait = 10

# Has your network found?
wifiFound = False

# Is the network connected?
wifiConnected = False

# Main program
splash("Network test")

##############################################################################
# Run the test
##############################################################################

# Setup WiFi
log("Setting up WiFi")
wifiNetwork = network.WLAN(network.STA_IF)
wifiNetwork.active(True)

# Scan networks until we find ours
while not wifiFound:

    log("Scanning networks...")
    networks = wifiNetwork.scan()

    for n in networks:
        networkName = n[0].decode("utf-8")
        if networkName != " " and networkName != "" :
            log("Discovered network", networkName)
            if networkName == WIFI_SSID:
                wifiFound = True

    log("Scan complete")

    # Not found our network, pause a while before re-scanning
    if not wifiFound:
        log("Failed to discover", WIFI_SSID)
        for i in range(5, 0, -1):
            log("Retry in {i}".format(i = i))
            sleep(1)

# Found our network - try to connect
log("Connecting to", WIFI_SSID)
wifiNetwork.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for network connection (wifiMaxWait seconds)
while wifiMaxWait > 0:

    # If we are no longer connecting break out the while loop
    if wifiNetwork.status() != network.STAT_CONNECTING:
        break

    wifiMaxWait -= 1
    log("Waiting for connection", wifiMaxWait)
    sleep(1)

# Handle the connection status
if wifiNetwork.status() != network.STAT_GOT_IP:

    # Didn't get an I.P so not connected
    wifiConnected = False

    # Wrong password or other error
    if wifiNetwork.status() == network.STAT_WRONG_PASSWORD:
        log("Network connection failed", "Wrong password")
    else:
        log("Network connection failed status", wifiNetwork.status())
else:
    # Got an I.P and connected
    wifiConnected = True
    wifiAddress = wifiNetwork.ifconfig()[0]
    log("Connected with I.P", wifiAddress)

if not wifiConnected:
    log("Could not download URL, no network connection.")
    exit()

# Download a page from the internet
log("Getting URL", TEST_URL)
try:
    r = urequests.get(TEST_URL)
    log("Downloaded content", r.content)
    r.close()
except OSError as err:
    log("Could not download from URL")
    log("OS error : ", err)

log("Test complete.")
