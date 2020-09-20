"""
Project Name : Home Weather Station
Purpose : Get values from Friebase and display on LCD
Created on : 20 Sep 2020
Created by : Sashwat K <sashwat0001@gmail.com>
Revision : 3
Last Updated by : Sashwat K <sashwat0001@gmail.com>
Last updated on : 20 Sep 2020
"""

# import RPi_I2C_driver # RPi LCD driver
from time import * # Time library
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

firebaseObject = pyrebase.initialize_app(configurationForFirebase)  # firebase connection object
databaseObject = firebaseObject.database()  # firebase database initialisation

# mylcd = RPi_I2C_driver.lcd() # Initialise LCD driver

def getValuesFromFirebase():
    listData = []
    listData.append(databaseObject.child(
                "sensor-values").child("cng").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("air_quality_index").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("lpg").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("smoke").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("co").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("rain_sensor").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("dht22_temperature").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("dht22_humidity").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("dht22_heat_index").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("bmp280_temperature").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("bmp280_pressure").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("bmp280_altitude").get().val())
    
    return listData

# Main Definition
def main():
    try:
        print("Home Weather Station LCD display driver...")
        print("Developed by Sashwat K")
        print("Initialising display..")

        while True:
            valueList = getValuesFromFirebase()
            print(valueList)

    except (KeyboardInterrupt, SystemExit): # for handling ctrl+c
        print("Closing the program")

if __name__ == "__main__":
    main()