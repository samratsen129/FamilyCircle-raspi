from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import grovepi
from grove_rgb_lcd import *

pnconf = PNConfiguration()
pnconf.publish_key = "demo"
pnconf.subscribe_key = "demo"
pnconf.enable_subscribe = True

pubnub = PubNub(pnconfig)
channel = "sbda0_987654321"
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

class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        print("status changed: %s" % status)

    def message(self, pubnub, message):
        grovepi.digitalWrite(buzzer,1)
        setText(value)
        if message == "red":
                setRGB(255,0,0)
        elif message == "green":
                setRGB(0,255,0)
        elif message == "green":
                setRGB(0,0,255)

    def presence(self, pubnub, presence):
        pass

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

my_listener = MyListener()
pubnub.add_listener(my_listener)
pubnub.subscribe().channels(channel).execute()

#pubnub.subscribe(
#        channel2,
#        callback = callbackInt)

