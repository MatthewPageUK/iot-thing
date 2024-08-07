#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___ 
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  A simple web server
#
#  @TODO 
#
import network
import socket
import re
import gc
from time import sleep

class ThingServer:

    # Create the server instance
    def __init__(self, logger, sensors, config):
        
        self.logger = logger
        self.sensors = sensors
        self.config = config
        self.logger.write('Setting up web server')
        
        # Create a socket to listen on
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.listen(1)
        
        # Don't let the socket block code execution, we have things to do
        self.s.setblocking(False)
        
        self.logger.write(' + Listening on port ' + str(self.addr[1]))
    
    # Route a request and return the response data
    #
    def routeRequest(self, request):

        if re.search("GET /settings HTTP", str(request)):
            # Settings page
            self.logger.write(' + Routed to settings.html')
            f = open('settings.html', 'r')
            response = f.read()
            f.close()
            
        elif re.search("GET /data HTTP", str(request)):
            # Ajak request for data, return JSON
            self.logger.write(' + Routed to data')
            response = self.sensors.getJson()
            
        else:
            # Dashboard view
            self.logger.write(' + Routed to index.html')
            f = open('dashboard.html', 'r')
            response = f.read()
            f.close()
            
        return response
    
    # Check for connection and respond
    def checkConnection(self):
        
        try:
            # Is there a connection waiting
            cl, addr = self.s.accept()
            self.logger.write('Client connected from ' + str(addr[0]))

            # Set the socket to blocking while we deal with it (questionable)
            cl.setblocking(True)
            
            # Receive the request data
            request = cl.recv(1024)

            # Log the request
            # logger.write(' + ' + str(request))

            # Get the response from the router
            #response = self.routeRequest(request)
            
            if re.search("GET /settings HTTP", str(request)):
                # Settings page
                self.logger.write(' + Routed to settings.html')
                f = open('settings.html', 'r')
                response = f.read()
                f.close()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
                cl.sendall(str(response))                 
                
            elif re.search("GET /data HTTP", str(request)):
                # Ajak request for data, return JSON
                self.logger.write(' + Routed to data')
                response = self.sensors.getJson()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
                cl.sendall(str(response))                 
                
            else:
                # Dashboard view
                self.logger.write(' + Routed to index.html')
                #f = open('dashboard.html', 'r')
                #response = f.read()
                #f.close()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html; charset=utf-8\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
                f = open('dashboard.html', 'r')
                while True:
                    chunk = f.read(5024)
                    if not chunk:
                        break
                    cl.sendall(str(chunk))
                cl.close()
                f.close()                
            
            # Send the response
            #cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
            #cl.sendall(str(response))        

            # Free up the blocking so we can continue to do other tasks ?
            # cl.setblocking(False)
            
            # Close the connection
            # cl.close()
            self.logger.write(' + Response sent')
         
            # Clean up memory
            response = None
            gc.collect()
             
            # Give it time to process the connection (fixed random issues)
            sleep(0.5)
     
        except OSError as e:
            nocon = True
