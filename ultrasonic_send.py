# GrovePi + Grove Ultrasonic Ranger
# Pubnub Import
#time
import grovepi
from grovepi import *
from pubnub import Pubnub
import os
import time
from m2x.client import M2XClient
import requests.packages.urllib3

#supress some very much needing security warnings-yolo
requests.packages.urllib3.disable_warnings()

# Connect the Grove Ultrasonic Ranger to digital port D3
# SIG,NC,VCC,GND
ultrasonic_ranger = 5
button=2
grovepi.pinMode(button,"INPUT")
#Setup connections to pubnub
pubnub = Pubnub(
        publish_key = "pub-c-090357d1-f0ff-4d6f-8c22-4e792d4a19fc",
        subscribe_key = "sub-c-28471b50-f917-11e5-8916-0619f8945a4f")
channel = "okButton"
#Setup M2X
client = M2XClient(key='5ad8f4935a732bc0857abacaf7acf425')
device = client.device('6eaa648010edfa6e1f63d915c5a683c3')
stream = device.stream('distance_stream')

#Read value from Grove Ultrasonic
def ultrasonicRead(pin):
        write_i2c_block(address,uRead_cmd+[pin,0,0])
        time.sleep(.2)
        read_i2c_byte(address)
        number = read_i2c_block(address)
#       print type(number)
        if type(number) is list:
                return (number[1]*256+number[2])
        return -1

while True:
    try:
        # Read distance value from Ultrasonic
        uSDist =  ultrasonicRead(ultrasonic_ranger)
#       print uSDist
        if(uSDist > 0):
                stream.add_value(int(uSDist))

        #read the button
        buttonValue = grovepi.digitalRead(button)
#       print buttonValue
        if buttonValue > 0:
                pubnub.publish(channel,
                        message = "reset")
#       if uSDist < 10:
#               pubnub.publish(channel,
#                       message = "on")
#               stream.add_value(int(uSDist))
#               print "less 10: %d" % (uSDist)
#       else:
#                pubnub.publish(channel,
#                        message = "off")
#               stream.add_value(int(uSDist))
#               print "not less 10: %d" % (uSDist)

        time.sleep(.5)
    except TypeError:
        print "Error"
    except IOError:
        print "Error"
