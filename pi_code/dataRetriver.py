"""
Project Name : Home Weather Station
Purpose : To get the values from UNO, log it and save it to firebase
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
from datetime import datetime, timedelta  # for date and time
from time import sleep # For beautification

load_dotenv()  # load environment (.env) file

# configuration for connection
configurationForFirebase = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "storageBucket": os.getenv("storageBucket"),
}

firebaseObject = pyrebase.initialize_app(configurationForFirebase)  # firebase connection object
databaseObject = firebaseObject.database()  # firebase database initialisation

ser = serial.Serial(os.getenv("usbPortName"),9600) # Serial port opened for communicating with UNO

logging.basicConfig(filename="app.log", level=logging.DEBUG,format="[%(asctime)s, %(message)s]", datefmt="%d/%m/%Y, %H:%M:%S")

# Definition to convert Serial output to string
def convertSerialToList(string):
    li = list(string.split(","))
    return li

# Definition to log sensor data
def dataLogging(inputData):
    logging.debug(inputData)

# Definition to store data in firebase
def sendDataToFireBase(inputData):
    try:
        now = datetime.now()  # get current time
        logTime = str(now.strftime("%H:%M:%S")) # convert to hour:minute:second
        logDate = str(now.strftime("%Y/%m/%d")) # convert to year/month/day

        theStoreValues = {"cng": inputData[0],
             "air_quality_index": inputData[1],
             "lpg": inputData[2],
             "smoke": inputData[3],
             "rain_sensor": inputData[5],
             "dht22_temperature": inputData[6],
             "dht22_humidity": inputData[7], 
             "dht22_heat_index": inputData[8],}

        databaseObject.child("sensor-values").update(theStoreValues)
        databaseObject.child("log").child(logDate).child(logTime).set(theStoreValues)
    except:
        pass

# Main Definition
def main():
    try:
        print("Home Wather Monitoring System..")
        print("Developed by Sashwat K <sashwat0001@gmail.com>")
        print("Initialisating sensors....")
        sleep(1)
        print("Initialisation complete....")
        while True: # for running forever
            read_serial = ser.readline().strip().decode("utf-8")
            theDataList = convertSerialToList(read_serial)
            if len(theDataList) == 8:
                dataLogging(theDataList)
                sendDataToFireBase(theDataList)
    except (KeyboardInterrupt, SystemExit): # for handling ctrl+c
        print("Releasing sensors..")
        sleep(1)
        print("Closing firebase connection..")
        sleep(1)
        print("Closing program..")

if __name__ == "__main__":
    main()