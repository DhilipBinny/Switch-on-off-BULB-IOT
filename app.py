import json
from flask import Flask, request, make_response, jsonify
import requests
import pyrebase

app = Flask(__name__)
log = app.logger

#firebase credentials 
config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


@app.route('/', methods=['POST'])
def webhook():
   req = request.get_json(silent=True, force=True)

   intent_name = req["queryResult"]["intent"]["displayName"]

   bulb_colour = req.get("queryResult").get("parameters").get("color")
   action_needed = req.get("queryResult").get("parameters").get("on_off")

   initial_bulb_state_dict = db.child("bulbs").get().val()
   
#    print(initial_bulb_state_dict)
#    print(bulb_dict.get(bulb_colour)) 

   bulb_dict = {
    "red": "bulb1",
    "green":"bulb2"
    }  

   # Braching starts here
   if intent_name == 'Bulb_Action':
        bulb_state = initial_bulb_state_dict[(bulb_dict[bulb_colour])]
        if action_needed == 'off':
            if bulb_state == "0" :
                response_text = "The {} bulb is already in off condition.".format(bulb_colour)
            else:
                db.child("bulbs").update({ bulb_dict[bulb_colour] : "0"})
                response_text = "The {} bulb is switched off.".format(bulb_colour)

        elif action_needed == "on":
            if bulb_state == "1" :
                response_text = "The {} bulb is already in on condition.".format(bulb_colour)
            else:
                db.child("bulbs").update({ bulb_dict[bulb_colour]  : "1"})           
                response_text = "The bulb {} is switched on.".format(bulb_colour)
        else:
            response_text = "invalid condition specified."
        

   else:
       response_text = "No intent matched"
   # Branching ends here

   # Finally sending this response to Dialogflow.
   return make_response(jsonify({'fulfillmentText': response_text}))



if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)
