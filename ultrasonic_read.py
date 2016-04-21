from pubnub import Pubnub
import grovepi
from grove_rgb_lcd import *

pubnub = Pubnub(
        publish_key = "pub-c-090357d1-f0ff-4d6f-8c22-4e792d4a19fc",
        subscribe_key = "sub-c-28471b50-f917-11e5-8916-0619f8945a4f")
channel = "pi-atthack-04162016";
channel2 = "okButton"

# Connect the Grove LED  to digital port D4
# SIG,NC,VCC,GND
led=4
buzzer=8
#set led to output
grovepi.pinMode(led,"OUTPUT")
grovepi.pinMode(buzzer,"OUTPUT")
grovepi.digitalWrite(led,0)
grovepi.digitalWrite(buzzer,0)
setText('ready')
setRGB(255,255,255)


def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))


def callback(message, channel):
        type = message['type']
        value =  message['value']
        if type == "panic":
#               grovepi.digitalWrite(led,1)
#               output = "Danger Will\nRobinson!"
                setText(value)
                setRGB(255,0,0)
                grovepi.digitalWrite(buzzer,1)
        elif type == "distance_stream":
#               grovepi.digitalWrite(led,1)
                output = "INTRUDER!\nDistance: "+str(value)+"cm"
                setText(output)
                setRGB(255,0,0)
                grovepi.digitalWrite(buzzer,1)
        elif type == "door":
                grovepi.digitalWrite(led,1)
                output = "Door open"
                setText(output)
                setRGB(0,255,0)
                grovepi.digitalWrite(buzzer,1)
                time.sleep(4)
                grovepi.digitalWrite(led,0)
                output = "Door closed"
                setText(output)
                setRGB(255,255,255)
                grovepi.digitalWrite(buzzer,0)
                time.sleep(5)
                setText("ready")

def callbackInt(message, channel):
        if message == "reset":
                grovepi.digitalWrite(led,0)
                grovepi.digitalWrite(buzzer,0)
                setText('ready')
                setRGB(255,255,255)

pubnub.subscribe(
        channel,
        callback = callback)
pubnub.subscribe(
        channel2,
        callback = callbackInt)

