# # Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client

# # Find your Account SID and Auth Token in Account Info and set the environment variables.
# # See http://twil.io/secure
# account_sid = 'ACe0a977fae42fe85c925bb4bd3eeaf0f1' # replace later with os.environ[]
# auth_token = '91348d25f4044be9d69bdd9c2ed3db9a' # replace later with os.environ[]
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     body='Hi there',
#     from_='+14793244060',
#     to='+12032166345'
# )

# print(message.sid)

import os
from twilio.rest import Client

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

account_sid = 'ACe0a977fae42fe85c925bb4bd3eeaf0f1' # replace later with os.environ[]
auth_token = '91348d25f4044be9d69bdd9c2ed3db9a' # replace later with os.environ[]
client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Hi there',
    from_='+14793244060',
    to='+12032166345'
)

# starting chess board
start_board = "" 

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None) 
    client_phone = request.values.get('from', None)

    # Start our TwiML response
    resp = MessagingResponse() 

    # check database to see if there is already a game going
    if client_phone in databse :

    elif 
    # Determine the right reply for this message
    if body == "Let's play chess!":
        resp.message(start_board)
    elif:


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)





###############################################################################################################################
# TWILIO EXAMPLE CODE
###############################################################################################################################

###############################################################################################################################
# SEND SMS MESSAGES
###############################################################################################################################

# from flask import Flask, request, redirect
# from twilio.twiml.messaging_response import MessagingResponse

# app = Flask(__name__)

# @app.route("/sms", methods=['GET', 'POST'])
# def incoming_sms():
#     """Send a dynamic reply to an incoming text message"""
#     # Get the message the user sent our Twilio number
#     body = request.values.get('Body', None)

#     # Start our TwiML response
#     resp = MessagingResponse()

#     # Determine the right reply for this message
#     if body == 'hello':
#         resp.message("Hi!")
#     elif body == 'bye':
#         resp.message("Goodbye")

#     return str(resp)

# if __name__ == "__main__":
#     app.run(debug=True)

###############################################################################################################################
# SEND MMS MESSAGES
###############################################################################################################################

# from flask import Flask
# from twilio.twiml.messaging_response import MessagingResponse

# app = Flask(__name__)


# @app.route("/sms", methods=['GET', 'POST'])
# def sms_reply():
#     """Respond to incoming calls with a MMS message."""
#     # Start our TwiML response
#     resp = MessagingResponse()

#     # Add a text message
#     msg = resp.message("The Robots are coming! Head for the hills!")

#     # Add a picture message
#     msg.media(
#         "https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg"
#     )

#     return str(resp)


# if __name__ == "__main__":
#     app.run(debug=True)

###############################################################################################################################
# SEND BASIC MESSAGES
###############################################################################################################################

# from flask import Flask, request, redirect
# from twilio.twiml.messaging_response import MessagingResponse

# app = Flask(__name__)

# @app.route("/sms", methods=['GET', 'POST'])
# def sms_reply():
#     """Respond to incoming calls with a simple text message."""
#     # Start our TwiML response
#     resp = MessagingResponse()

#     # Add a message
#     resp.message("The Robots are coming! Head for the hills!")

#     return str(resp)

# if __name__ == "__main__":
#     app.run(debug=True)