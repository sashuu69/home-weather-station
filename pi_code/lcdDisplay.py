"""
Project Name : Home Weather Station
Purpose : Get values from Friebase and display on LCD
Created on : 20 Sep 2020
Created by : Sashwat K <sashwat0001@gmail.com>
Revision : 3
Last Updated by : Sashwat K <sashwat0001@gmail.com>
Last updated on : 20 Sep 2020
"""

import RPi_I2C_driver # RPi LCD driver
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

systemLCD = RPi_I2C_driver.lcd() # Initialise LCD driver

# Definition to fetch values from FireBase
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
                "sensor-values").child("rain_sensor").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("dht22_temperature").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("dht22_humidity").get().val())
    listData.append(databaseObject.child(
                "sensor-values").child("dht22_heat_index").get().val())
    return listData

def displayValuesInLCDInitialise():
    systemLCD.lcd_clear()
    systemLCD.lcd_display_string_pos("Home Weather", 1,2)
    systemLCD.lcd_display_string_pos("Station", 2,4)
    sleep(2)
    systemLCD.lcd_display_string_pos("Developed By", 1,2)
    systemLCD.lcd_display_string_pos("Sashwat K", 2,3)

def displayValuesInLCDLoop(listData):
    systemLCD.lcd_clear()
    systemLCD.lcd_display_string_pos(str("CNG: " + listData[0] + " PPM"), 1,1)
    systemLCD.lcd_display_string_pos(str("AQI: " + listData[1] + " PPM"), 2,1)
    sleep(2)
    systemLCD.lcd_clear()
    systemLCD.lcd_display_string_pos(str("LPG: " + listData[2] + " PPM"), 1,1)
    systemLCD.lcd_display_string_pos(str("Smoke: " + listData[3] + " PPM"), 2,1)
    sleep(2)
    systemLCD.lcd_clear()
    systemLCD.lcd_display_string_pos(str("Rain: " + listData[5]), 1,1)
    systemLCD.lcd_display_string_pos(str("HI-D: " + listData[8]), 2,1)
    sleep(2)
    systemLCD.lcd_clear()
    systemLCD.lcd_display_string_pos(str("Temp-D: " + listData[6] + " C"), 1,1)
    systemLCD.lcd_display_string_pos(str("Hum-D: " + listData[7] + " %"), 2,1)
    sleep(2)

# Main Definition
def main():
    try:
        print("Home Weather Station LCD display driver...")
        print("Developed by Sashwat K")
        print("Initialising display..")
        displayValuesInLCDInitialise()

        while True:
            displayValuesInLCDLoop(getValuesFromFirebase())

    except (KeyboardInterrupt, SystemExit): # for handling ctrl+c
        systemLCD.lcd_clear()
        systemLCD.lcd_display_string_pos("Closing Program..",1,1)
        sleep(0.8)
        systemLCD.lcd_clear()
        print("Closing the program")

if __name__ == "__main__":
    main()
