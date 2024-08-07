#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___ 
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  Simple log written to file and std out
#
#  @TODO Error checking and exceptions
#  @TODO Check available storage, never fill up the space, 1 in 1 out if near full
#
import gc

class ThingLogger:

    # Create the logger instance
    def __init__(self, fileName='thing.log', clock=False):
        self.fileName = fileName
        self.clock = clock

    # Open, write and close the log file, print message
    def write(self, data='Example log'):
        logFile = open(self.fileName, 'a')
        logFile.write(self.getTime() + ', ' + str(data) + ', Mem=' + str(gc.mem_free()) + '\r\n')
        logFile.close()
        print(str(data))

    # Get the current time as a string
    def getTime(self):
        timestamp = self.clock.datetime()
        timestring = "%04d-%02d-%02d %02d:%02d:%02d" % (timestamp[0:3] + timestamp[4:7])
        return timestring
