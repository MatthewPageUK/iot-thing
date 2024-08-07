#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___ 
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
import micropython

from machine import Pin, I2C
from time import sleep
from pico_i2c_lcd import I2cLcd
import utime as time
import bme280
import network
import socket
import re
import gc
from picoredis import Redis
from thinglogger import ThingLogger
from thingsensors import ThingSensors
from configparser import ConfigParser
from thingserver import ThingServer

print(" __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___ ")
print("(  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)")
print(" )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.")
print("(_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/")
print("________________________________________________________________")
print(" ")


# The clock (probably wrong if it just turned on)
clock = machine.RTC()

# Read the config settings
config = ConfigParser()
config.read('thing.ini')

# Start the logger
logger = ThingLogger(config.get('LOG', 'FILE'), clock)
logger.write('Starting...')

# WiFi Settings
wifiMaxWait = config.get_int('WIFI', 'MAX_WAIT')
wifiConnected = False



# Setup the BME280 I2C
# @TODO error checking
logger.write('Setting up BME280')
bmeI2c = I2C(
    id=0,
    sda=Pin(config.get_int('BME280', 'SDA_PIN')),
    scl=Pin(config.get_int('BME280', 'SCL_PIN')),
    freq=config.get_int('BME280', 'FREQUENCY'))
bme = bme280.BME280(i2c=bmeI2c)
logger.write(' + Done')

#Setup the LCD I2C
logger.write('Setting up LCD Display')
lcdI2c = I2C(
    id=1,
    sda=Pin(config.get_int('LCD', 'SDA_PIN')),
    scl=Pin(config.get_int('LCD', 'SCL_PIN')),
    freq=config.get_int('LCD', 'FREQUENCY'))
lcd = I2cLcd(
    lcdI2c,
    0x3F,
    config.get_int('LCD', 'LINES'),
    config.get_int('LCD', 'COLUMNS'))
logger.write(' + Done')

def clear_lcd():
    lcd.move_to(0,0)
    lcd.putstr('                                ')
    
def splashScreen():
    lcd.move_to(2,0)
    lcd.putstr("Matt's Thing")
    lcd.move_to(6,1)
    lcd.putstr("v0.1")
    
def print_lcd(line1 = '                ', line2 = '                '):
    lcd.move_to(0, 0)
    lcd.putstr(line1)
    lcd.move_to(0, 1)
    lcd.putstr(line2)

# Setup WiFi connection
logger.write('Setting up network')
wifiNetwork = network.WLAN(network.STA_IF)
wifiNetwork.active(True)
wifiNetwork.connect(config.get('WIFI', 'SSID'), config.get('WIFI', 'PASSWORD'))
logger.write(' + Done')
 
# Wait for network connection (wifiMaxWait seconds)
while wifiMaxWait > 0:
    if wifiNetwork.status() < 0 or wifiNetwork.status() >= 3:
        break
    wifiMaxWait -= 1
    logger.write(' + Waiting for connection')
    print_lcd('Connecting ' + str(wifiMaxWait) + ' ')
    time.sleep(1)
 
# Handle connection status
if wifiNetwork.status() != 3:
    wifiConnected = False
    logger.write(' + Network connection failed - ' + str(wifiNetwork.status()))
    print_lcd('Connection failed')
    time.sleep(2)
else:
    wifiConnected = True
    status = wifiNetwork.ifconfig()
    logger.write(' + Connected with address ' + status[0])
    print_lcd('Connected')
    time.sleep(2)


lcd.clear()
 
# Setup the on board LED
led = Pin("LED", Pin.OUT)

# Setup the button as an Input and pull the current down on it
button = Pin(config.get_int('BUTTON', 'PIN'), Pin.IN, Pin.PULL_DOWN)

# Setup the photoresistor with analogue to digital converter
photoResistor = machine.ADC(config.get_int('PHOTO_RESISTOR', 'PIN'))

# Create the ThingSensors
sensors = ThingSensors(config = config, logger = logger, bme280 = bme, photoResistor = photoResistor)


server = ThingServer(logger, sensors, config)

logger.write('Setup Completed')

lcd.backlight_on()
led.value(0)
splashScreen()
sleep(2)
clear_lcd()

# Setup the defaul display mode and settings
displayMode = 'all'
displayRefresh = config.get_int('THING', 'POLL_RATE')
displayCount = displayRefresh

# Setup the Redis API

#if wifiConnected:
#    r = Redis(host = 'redis-17546.c1.eu-west-1-3.ec2.cloud.redislabs.com', port = 17546)
#    r.auth('PiknebF3hYBfcK1dvzacNgE6Zq5YWVXk')
        
#
# Main program loop
#
while True:

    # Check if there is a connection waiting and deal with it
    server.checkConnection()

    # Check if the display needs refreshing (polling rate)
    if displayCount > displayRefresh:
        
        logger.write('Poll')

        # Log the data to Redis
        if wifiConnected:
            #r.xadd('thingStream', '*', 'thing', str(serialNumber), 'temperature', str(sensors.temperature()), 'pressure', str(sensors.pressure()), 'humidity', str(sensors.humidity()), 'light', str(sensors.light()))
            pass
        else:
            # Log the data to local storage
            # @TODO Sort out the time issue, no time on reboot?
            
            # Offline cache settings
            offlineFile = open(config.get('LOCAL_STORAGE', 'FILE'), 'a')            
            timestamp=clock.datetime()
            timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])
            offlineFile.write(timestring + ',' + str(sensors.temperature()) + '\n')
            offlineFile.close()

        led.value(1)
        displayCount = 0
        lcd.clear()

        # Choose which screen to display
        if displayMode == 'info':
            splashScreen()
            
        if displayMode == 'net':
            print_lcd('Network :')
            if wifiConnected:
                print_lcd('', status[0])
            else:
                print_lcd('', 'No connection')
                
        if displayMode == 'temp':
            print_lcd('Temperature :', sensors.temperature(True))
            
        if displayMode == 'pres':
            print_lcd('Pressure :', sensors.pressure(True))            
            
        if displayMode == 'humi':
            print_lcd('Humidity :', sensors.humidity(True))

        if displayMode == 'light':
            print_lcd('Light :', str(sensors.light()) + ' ' + sensors.lightDark())

        if displayMode == 'all':
            print_lcd(sensors.temperature(True), sensors.pressure(True))
            lcd.move_to(config.get_int('LCD', 'COLUMNS') - len(sensors.humidity(True)),0)
            lcd.putstr(sensors.humidity(True))     
            lcd.move_to(config.get_int('LCD', 'COLUMNS') - len(sensors.lightDark()),1)
            lcd.putstr(sensors.lightDark())

        gc.collect()
        led.value(0)
            
    # Check if the button was pressed
    if button.value():

        # Cycle through the displays
        if displayMode == 'all':
            displayMode = 'temp'
        elif displayMode == 'temp':
            displayMode = 'pres'
        elif displayMode == 'pres':
            displayMode = 'humi'
        elif displayMode == 'humi':
            displayMode = 'light'
        elif displayMode == 'light':
            displayMode = 'info'            
        elif displayMode == 'info':
            displayMode = 'net'
        elif displayMode == 'net':
            displayMode = 'all'            
            
        # Force a display refresh immediatly
        displayCount = displayRefresh
        
        # Debounce
        sleep(0.5)

    displayCount += 1
    
    # Everything runs at 10 fps
    sleep(0.1)
        
    