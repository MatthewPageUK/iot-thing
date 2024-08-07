#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___ 
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  A wrapper for the sensors
#
#  @TODO Error checking on reading values
#
import re

class ThingSensors:

    # Create the sensors instance
    def __init__(self, config=None, logger=None, bme280=None, photoResistor=None):
        self.config = config
        self.logger = logger
        self.bme280 = bme280
        self.photoResistor = photoResistor

    # Get the temperature reading from the BME280 sensor
    def temperature(self, formatted=False):
        t = re.sub(r'[^0-9.]', '', str(self.bme280.values[0]))
        if formatted:
            return str(t) + 'C'
        else:        
            return float(t)

    # Get the pressure reading from the BME280 sensor
    def pressure(self, formatted=False):
        p = re.sub(r'[^0-9.]', '', str(self.bme280.values[1]))
        if formatted:
            return str(p) + 'hPa'
        else:        
            return float(p)

    # Get the humidity reading from the BME280 sensor
    def humidity(self, formatted=False):
        h = re.sub(r'[^0-9.]', '', str(self.bme280.values[2]))
        if formatted:
            return str(h) + '%'
        else:
            return float(h)

    # Get the light reading from the photo resistor
    def light(self, formatted=False):
        l = self.photoResistor.read_u16()
        return float(l)

    # Return light or dark text based on the light sensor
    def lightDark(self, lightText='Light', darkText='Dark'):
        if(self.light() < 60000):
            return lightText
        else:
            return darkText

    def getJson(self):
        json = '{{"t": {t}, "p": {p}, "h": {h}, "l": {l}, "n": "{n}", "v": "0.1", "s": "{s}", "r": {r}, "ts": "{ts}" }}'
        response = json.format(
            t=self.temperature(),
            p=int(self.pressure()),
            h=int(self.humidity()),
            l=self.light(),
            n=self.config.get('THING', 'NAME'),
            s=self.config.get('THING', 'SERIAL_NUMBER'),
            r=self.config.get('API', 'REFRESH'),
            ts=self.logger.getTime())
        return response
