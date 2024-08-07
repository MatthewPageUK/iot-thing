#   __  __    __   ____  ____/ ___    ____  _   _  ____  _  _  ___
#  (  \/  )  /__\ (_  _)(_  _)/ __)  (_  _)( )_( )(_  _)( \( )/ __)
#   )    (  /(__)\  )(    )(  \__ \    )(   ) _ (  _)(_  )  (( (_-.
#  (_/\/\_)(__)(__)(__)  (__) (___/   (__) (_) (_)(____)(_)\_)\___/
#
#  Raspberry Pi Pico-W IOT Sensor
#
#  A simple file rotator. Supply the required settings and returns
#  the name of a file to write to. If files are oversized they are
#  rotated, only keep max files...
#
#  @TODO
#
import os
import network
import socket
import re
import gc
from time import sleep


def getLastestRotation(files):
    """Get the last rotation number from the files

    Parameters
    ----------
    files
        The list of files in the data directory

    Returns
    -------
        int
    """
    rotation = 1
    if files and len(files) > 0:
        for f in files:
            rot = re.match('\d+|$', f).group(0)
            rot = int(rot)
            if rotation <= rot:
                rotation = rot
    return rotation

def getFirstRotation(files):
    """Get the first rotation number from the files

    Parameters
    ----------
    files
        The list of files in the data directory

    Returns
    -------
        int
    """
    rotation = 0
    if files and len(files) > 0:
        for file in files:
            rot = re.match('\d+|$', file).group(0)
            rot = int(rot)
            if rotation > rot or rotation == 0:
                rotation = rot
    return rotation



def getFile(DATA_DIRECTORY, FILE_NAME, MAX_FILE_SIZE, MAX_FILES):

    try:
        # Get a list of files in the data directory
        files = os.listdir(DATA_DIRECTORY)

    except Exception as err:
        # Couldn't get the list
        log("Creating data folder", DATA_DIRECTORY)
        try:
            # Try creating the directory
            directory = os.mkdir(DATA_DIRECTORY)
            files = os.listdir(DATA_DIRECTORY)

        except Exception as err:
            # Can't continue without a data folder
            log("Could not create the data folder", "Stopping")
            exit()

    # Get the latest rotation number
    rotation = getLastestRotation(files)

    # The full filename of our data file 'test-data/1-test.data'
    fileName = "{d}/{r}-{f}".format(d = DATA_DIRECTORY, r = rotation, f = FILE_NAME)
    fileSize = 0

    try:
        # Get the size of our data file
        fileSize = os.stat(fileName)[6]/1000
        log("Data file size", "{s}Kb".format(s = fileSize))
    except Exception as err:
        # It may not exist, that's ok
        log("Data file size", "0Kb")

    # Check the size is more than the max
    if fileSize > MAX_FILE_SIZE:

        # Rotate the data file
        log("File needs rotating", "{f} {s}Kb".format(f = fileName, s = fileSize))
        if len(files) > 0:

            # Examine each file to see if there is one we can append to
            # or we need to create a new one - why? on start up ?
            for f in files:

                # The data file we're looking at
                dataFile = DATA_DIRECTORY + "/" + f
                fileExists = True

                # Get the size
                try:
                    dataFileSize = os.stat(dataFile)[6]/1000
                    log("File size" , "{f} {s}Kb".format(f = dataFile, s = dataFileSize))
                except Exception as err:
                    log("File doesnt exist...", f)
                    fileExists = False

                if fileExists:
                    # Extract the rotation number from the file
                    rot = re.match('\d+|$', f).group(0)
                    rot = int(rot)
                    log("File rotation number", rot)

                    if rotation <= rot:
                        # If the rot is bigger than current setting
                        if dataFileSize > MAX_FILE_SIZE:
                            # This file is oversized, set rotation number to one after this one
                            rotation = rot + 1
                            log("New rotation number", rot + 1)

                            # We're creating a new file so need to check MAX_FILES
                            log("Total files", len(files))
                            if len(files) >= MAX_FILES:
                                # Delete the first file
                                firstRot = getFirstRotation(files)
                                log("FIRST ROT", firstRot)
                                deleteFile = "{d}/{r}-{f}".format(d = DATA_DIRECTORY, r = firstRot, f = FILE_NAME)
                                log("Deleting data file", deleteFile)
                                os.remove(deleteFile)

                        else:
                            # We can use this file
                            rotation = rot
                            log("Re-opening old file", dataFile)

        # By now we have a correct rotation number.
        # It's either a new one or an existing one that can be appendd to
        fileName = "{d}/{r}-{f}".format(d = DATA_DIRECTORY, r = rotation, f = FILE_NAME)

    # Finally we can open and write to the file :)
    log("Opening data file", fileName)
    logFile = open(fileName, 'a')

    log("Writing data....", count)
    logFile.write(str(count) + DATA_STRING + '\r\n')
    logFile.close()
    log("Closed file")

    count += 1

    # We need a sleep after all that...
    sleep(5)
