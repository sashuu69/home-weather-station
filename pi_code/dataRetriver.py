"""
Project Name : Home Weather Station
Purpose : To get the values from UNO and log it
Created on : 17 Sep 2020
Created by : Sashwat K <sashwat0001@gmail.com>
Revision : 3
Last Updated by : Sashwat K <sashwat0001@gmail.com>
Last updated on : 18 Sep 2020
"""

import serial # Library for serial communication
import logging # Library for logging
import pyrebase  # python library for firebase
from dotenv import load_dotenv  # for accessing environment (.env) file
import os  # for supporting dotenv

load_dotenv()  # load environment (.env) file

# configuration for connection
configurationForFirebase = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "storageBucket": os.getenv("storageBucket"),
}

firebaseObject = pyrebase.initialize_app(
    configurationForFirebase)  # firebase connection object
databaseObject = firebaseObject.database()  # firebase database initialisation

ser = serial.Serial("/dev/ttyACM0",9600)

logging.basicConfig(filename="app.log", level=logging.DEBUG,format="[%(asctime)s, %(message)s]", datefmt="%d/%m/%Y, %H:%M:%S")

def convertSerialToList(string):
    li = list(string.split(","))
    return li

def dataLogging(inputData):
    logging.debug(inputData)

def main():
    while True:
        read_serial = ser.readline().strip().decode("utf-8")
        theDataList = convertSerialToList(read_serial)
        if len(theDataList) == 12:
            dataLogging(theDataList)

if __name__ == "__main__":
    main()