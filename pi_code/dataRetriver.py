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
from datetime import datetime, timedelta  # for date and time

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

ser = serial.Serial("/dev/ttyACM0",9600)

logging.basicConfig(filename="app.log", level=logging.DEBUG,format="[%(asctime)s, %(message)s]", datefmt="%d/%m/%Y, %H:%M:%S")

def convertSerialToList(string):
    li = list(string.split(","))
    return li

def dataLogging(inputData):
    logging.debug(inputData)

def sendDataToFireBase(inputData):
    try:
        now = datetime.now()  # get current time
        logTime = str(now.strftime("%H:%M:%S")) # convert to hour:minute:second
        logDate = str(now.strftime("%Y/%m/%d")) # convert to year/month/day

        databaseObject.child("sensor-values").update(
            {"cng": inputData[0],
             "air_quality_index": inputData[1],
             "lpg": inputData[2],
             "smoke": inputData[3],
             "co": inputData[4],
             "rain_sensor": inputData[5],
             "dht22_temperature": inputData[6],
             "dht22_humidity": inputData[7], 
             "dht22_heat_index": inputData[8],
             "bmp280_temperature": inputData[9],
             "bmp280_pressure": inputData[10],
             "bmp280_altitude": inputData[11],}
        )

        databaseObject.child("log").child(logDate).child(logTime).set(
            {"cng": inputData[0],
             "air_quality_index": inputData[1],
             "lpg": inputData[2],
             "smoke": inputData[3],
             "co": inputData[4],
             "rain_sensor": inputData[5],
             "dht22_temperature": inputData[6],
             "dht22_humidity": inputData[7], 
             "dht22_heat_index": inputData[8],
             "bmp280_temperature": inputData[9],
             "bmp280_pressure": inputData[10],
             "bmp280_altitude": inputData[11],}
        )
    except:
        pass

def main():
    while True:
        read_serial = ser.readline().strip().decode("utf-8")
        theDataList = convertSerialToList(read_serial)
        if len(theDataList) == 12:
            dataLogging(theDataList)
            sendDataToFireBase(theDataList)

if __name__ == "__main__":
    main()