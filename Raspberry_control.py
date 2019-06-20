import pyrebase
import RPi.GPIO as GPIO
import time

#Firebase credentials
config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# GET bulbs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_dict = {
    "bulb1":24,
    "bulb2":23
}

on = GPIO.HIGH
off = GPIO.LOW

initial_bulb_state_dict = db.child("bulbs").get().val()

def state_update(state_dct):

    for key in state_dct:
        if state_dct[key] == "1":
            GPIO.setup(pin_dict[key],GPIO.OUT)
            GPIO.output(pin_dict[key],on)

        if state_dct[key]=="0":
            GPIO.setup(pin_dict[key],GPIO.OUT)
            GPIO.output(pin_dict[key],off)

def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

    new_state_dict = message["data"]
    state_update(new_state_dict)

state_update(initial_bulb_state_dict)

my_stream = db.child("bulbs").stream(stream_handler)
