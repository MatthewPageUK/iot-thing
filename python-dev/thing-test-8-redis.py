#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  Redis data stream test.
#
#  Sets up the network and then attempts to send some data to the
#  Redis host. Repeats every 5 seconds.
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
    from picoredis import Redis
except ImportError:
    print("\nPlease save 'picoredis.py' file to your Thing before running the test\n\n")
    exit(0)
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

# Your Redis database
REDIS_HOST = "redis-17546.c1.eu-west-1-3.ec2.cloud.redislabs.com"
REDIS_PORT = 17546
REDIS_SECRET = "PiknebF3hYBfcK1dvzacNgE6Zq5YWVXk"

# How long between sending data
REDIS_INTERVAL = 5

##############################################################################
# Test setup
##############################################################################

# Setup the LED Pin
led = Pin('LED', Pin.OUT)

# Maximum time to wait for a network connection
wifiMaxWait = 10

# Was your network found
wifiFound = False

# Network connection status
wifiConnected = False

# How many times we've sent data to Redis
count = 0

# Main program
splash("Redis data stream test")

# Setup WiFi
log("Setting up WiFi")
wifiNetwork = network.WLAN(network.STA_IF)
wifiNetwork.active(True)
wifiNetwork.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for network connection (wifiMaxWait seconds)
while wifiMaxWait > 0:
    if wifiNetwork.status() < 0 or wifiNetwork.status() >= 3:
        break
    wifiMaxWait -= 1
    log("Waiting for connection {w}".format(w = wifiMaxWait))
    sleep(1)

# Handle connection status
if wifiNetwork.status() != 3:
    wifiConnected = False
    log("Network connection failed with status {s}".format(s = wifiNetwork.status()))
else:
    wifiConnected = True
    wifiAddress = wifiNetwork.ifconfig()[0]
    log("Connected")

# Setup the Redis connection
try:
    r = Redis(host = REDIS_HOST, port = REDIS_PORT)
    r.auth(REDIS_SECRET)
except Exception as err:
    log("Error connecting to Redis", err)
    r = False


##############################################################################
# Run the test
##############################################################################
while True:
    if wifiConnected:
        if r:
            try:
                # Send the data to Redis
                r.xadd('thingStream', '*', 'data', 'hello', 'count', str(count))
                log('Sent stream data to Redis', count)
                flash_led(led)
                count += 1
            except Exception as err:
                log("Error send data to Redis", err)
        else:
            log("No connection to Redis")
    else:
        log("No wifi connection")
        
    sleep(REDIS_INTERVAL)
