#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  API setup and test.
#
#  Sets up the network and then listens on port 80 for connections.
#  Responds with a simple HTTP request and message.
#
#  By           - Matthew Page
#  Credit       - Everyone who came before and wrote a how to guide
#  Version      - 0.1
#  Release date - 21st November 2022
#
from sys import exit
from time import sleep
import machine
import gc
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
led = machine.Pin('LED', machine.Pin.OUT)

# Maximum time to wait for a network connection
wifiMaxWait = 10

# Was your network found
wifiFound = False

# Network connection status
wifiConnected = False

# Main program
splash("API test")

# Setup WiFi
log("Setting up WiFi")
wifiNetwork = network.WLAN(network.STA_IF)
wifiNetwork.active(True)
wifiNetwork.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for network connection (wifiMaxWait seconds)
while wifiMaxWait > 0:
    if wifiNetwork.status() != network.STAT_CONNECTING:
        break
    wifiMaxWait -= 1
    log("Waiting for connection {w}".format(w = wifiMaxWait))
    sleep(1)

# Handle connection status
if wifiNetwork.status() != network.STAT_GOT_IP:
    wifiConnected = False
    log("Network connection failed with status {s}".format(s = wifiNetwork.status()))
    log("Please try running to 'thing-test-6-network.py' to debug your network connection")
    exit()
else:
    wifiConnected = True
    wifiAddress = wifiNetwork.ifconfig()[0]
    log("Connected")

##############################################################################
# Run the test
##############################################################################

# Open socket
try:
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
except Exception as err:
    log("Failed to open a socket", err)
    exit()

log('Listening on', addr)
log("Visit http://{a} to see your Thing".format(a = wifiAddress))
log(" ")

# Listen for connections
while True:
  try:
    cl, addr = s.accept()
    log('Client connected from', "{h}:{p}".format(h = addr[0], p = addr[1]))
    request = cl.recv(1024)
    for r in request.splitlines():
        log(" ", r.decode())

    request = str(request)

    # A basic HTML page response with some data from the Thing
    web_page = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title x-text="name">Test Thing</title>
                <script src="https://cdn.tailwindcss.com"></script>
                <script src="https://unpkg.com/alpinejs" defer></script>
                <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Neucha&family=Orbitron">
                <style type="text/tailwindcss">
                    @layer utilities {{
                        body {{
                            font-family: 'Neucha', serif;
                        }}
                        footer {{
                            font-family: 'Orbitron', serif;
                            @apply text-xs p-4 bg-green-900 text-lime-500 text-left border
                        }}
                    }}
                </style>
            </head>
            <body x-data="{{
                thing_id: '{id}',
                thing_date: '{date}',
                thing_memory: '{memory}'
            }}">
                <div class="fixed bg-gradient-to-b from-sky-300 via-amber-100 to-emerald-700 rounded-lg shadow-xl inset-8 flex">
                  <div class="m-auto w-80 text-center">
                    <h1 class="text-5xl mb-16">Welcome to<br />Thing API</h1>
                    <p class="mb-16">This is your API homepage</p>
                    <footer>
                        ID - <span x-text="thing_id"></span><br />
                        Date - <span x-text="thing_date"></span><br />
                        Memory - <span x-text="Math.floor(thing_memory/1000)"></span>Kb</footer>
                  </div>
                </div>
            </body>
        </html>
    """

    response = web_page.format(
        id = str(machine.unique_id()).replace("'", r"\'"),
        date = machine.RTC().datetime(),
        memory = gc.mem_free())

    log("Sending response")
    flash_led(led)
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
    log("Response sent")

  except OSError as e:
    cl.close()
    log('Connection closed')