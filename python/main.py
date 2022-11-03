from machine import Pin, I2C
from time import sleep
from pico_i2c_lcd import I2cLcd
import utime as time
import bme280
import network
from picoredis import Redis

import micropython

lcdi2c = I2C(id=1, scl=Pin(7), sda=Pin(6), freq=100000)
lcd = I2cLcd(lcdi2c, 0x3F, 2, 16)

bmei2c=I2C(id=0,sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=bmei2c)

def clear_lcd():
    lcd.move_to(0,0)
    lcd.putstr('                                ')
    
def splashScreen():
    lcd.move_to(2,0)
    lcd.putstr("Matt's Thing")
    lcd.move_to(6,1)
    lcd.putstr("v0.1") 

ssid = 'mattnet'
password = 'letmeout'
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
 
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
  if wlan.status() < 0 or wlan.status() >= 3:
    break
  max_wait -= 1
  
  print('waiting for connection...')
  
  spinner = '-' if spinner == '|' else '|'
  lcd.move_to(0, 0)
  lcd.putstr('Connecting ' + spinner + ' ' + max_wait + ' ')
  time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
   raise RuntimeError('network connection failed')
else:
  print('connected')
  status = wlan.ifconfig()
  print( 'ip = ' + status[0] )


lcd.clear()







devices = lcdi2c.scan()
if len(devices) == 0:
 print("No i2c device !")
else:
 print('i2c devices found:',len(devices))
for device in devices:
 print("At address: ",hex(device))



devices = bmei2c.scan()
if len(devices) == 0:
 print("No i2c device !")
else:
 print('i2c devices found:',len(devices))
for device in devices:
 print("At address: ",hex(device))
 
 


led = Pin("LED", Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
light = machine.ADC(27)

lcd.backlight_on()
led.value(0)
splashScreen()
sleep(2)
clear_lcd()

displayMode = 'all'
displayRefresh = 50
displayCount = displayRefresh


r = Redis(host = 'redis-17546.c1.eu-west-1-3.ec2.cloud.redislabs.com', port = 17546)
r.auth('PiknebF3hYBfcK1dvzacNgE6Zq5YWVXk')

while True:
    
    lightReading = light.read_u16()
    if(lightReading > 15000):
        lightText = 'Light'
    else:
        lightText = ' Dark'
    
    if displayCount > displayRefresh:
        
        micropython.mem_info()
        
        r.xadd('thingStream', '*', 'thing', '001', 'temperature', str(bme.values[0]), 'pressure', str(bme.values[1]), 'humidity', str(bme.values[2]), 'light', str(light.read_u16()))
        
        led.value(1)
        displayCount = 0
        
        if displayMode == 'info':
            splashScreen()
            
        if displayMode == 'temp':
            lcd.move_to(0,0)
            lcd.putstr('Temperature :')
            lcd.move_to(0,1)
            lcd.putstr(bme.values[0])
            
        if displayMode == 'pres':
            lcd.move_to(0,0)
            lcd.putstr('Pressure :')
            lcd.move_to(0,1)
            lcd.putstr(bme.values[1])            
            
        if displayMode == 'humi':
            lcd.move_to(0,0)
            lcd.putstr('Humidity :')
            lcd.move_to(0,1)
            lcd.putstr(bme.values[2])

        if displayMode == 'light':
            lcd.move_to(0,0)
            lcd.putstr('Light :')
            lcd.move_to(0,1)
            lcd.putstr(str(light.read_u16()) + '  ')

        if displayMode == 'all':
            lcd.move_to(0,0)
            lcd.putstr(bme.values[0])            
            lcd.move_to(0,1)
            lcd.putstr(bme.values[1])
            lcd.move_to(10,0)
            lcd.putstr(bme.values[2])     
            lcd.move_to(11,1)
            lcd.putstr(lightText)
            
        led.value(0)
        
    displayCount += 1
    
    if button.value():
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
            displayMode = 'all'            
            
        displayCount = displayRefresh
        sleep(0.5)
        lcd.clear()
    else:
        sleep(0.1)
        
    