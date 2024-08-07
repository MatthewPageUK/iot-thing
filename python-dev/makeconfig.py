#
# Make the default config file
#
import micropython
from configparser import ConfigParser

# Create a new config with some data
config = ConfigParser()

config.add_section('THING')
config.add_option('THING', 'SERIAL_NUMBER', '000001')
config.add_option('THING', 'NAME', 'Matt\'s Thing')
config.add_option('THING', 'POLL_RATE', '50')

config.add_section('BME280')
config.add_option('BME280', 'SDA_PIN', '0')
config.add_option('BME280', 'SCL_PIN', '1')
config.add_option('BME280', 'FREQUENCY', '400000')

config.add_section('LCD')
config.add_option('LCD', 'SDA_PIN', '6')
config.add_option('LCD', 'SCL_PIN', '7')
config.add_option('LCD', 'ADDRESS', '0x3F')
config.add_option('LCD', 'FREQUENCY', '100000')
config.add_option('LCD', 'LINES', '2')
config.add_option('LCD', 'COLUMNS', '16')

config.add_section('BUTTON')
config.add_option('BUTTON', 'PIN', '14')

config.add_section('PHOTO_RESISTOR')
config.add_option('PHOTO_RESISTOR', 'PIN', '27')

config.add_section('API')
config.add_option('API', 'PORT', '80')
config.add_option('API', 'SECRET', 'abcdefgh')

config.add_section('WIFI')
config.add_option('WIFI', 'SSID', 'mattnet')
config.add_option('WIFI', 'PASSWORD', 'letmeout')
config.add_option('WIFI', 'MAX_WAIT', '10')

config.add_section('LOCAL_STORAGE')
config.add_option('LOCAL_STORAGE', 'FILE', 'thing.data')

config.add_section('LOG')
config.add_option('LOG', 'FILE', 'thing.log')

config.add_section('REDIS')
config.add_option('REDIS', 'HOST', 'redis-17546.c1.eu-west-1-3.ec2.cloud.redislabs.com')
config.add_option('REDIS', 'PORT', '17546')
config.add_option('REDIS', 'SECRET', 'PiknebF3hYBfcK1dvzacNgE6Zq5YWVXk')

# Save it
config.write('thing.ini')
