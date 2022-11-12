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
    if client_phone in database:

        # retrieve current board state from database

        if client_board isn't empty:

            user_move = body

            # retrieve valid moves from stockfish
            valid_moves = ...

            if user_move in valid_moves:
                # find new board state given the user's move
                new_board = move(client_board, user_move)

                # get stockfish's move and all the user's new current possible moves
                valid_next_moves = ...
                board_reply = ... # board after stockfish's move
                
                
                # send stockfish's move to the user along with all their current possible next moves
                resp.message(board_reply)
                resp.message(valid_next_moves)

                # update database with new current board state
            else:
                resp.message("Invalid move, please send a valid move")
        elif body == "Let's play chess!":
            resp.message("Black or White?")
        elif body == "Black":
            # Send stockfish the starting board with them as the white player and receive their first move
            # Get valid user moves from stockfish from the starting board
            valid_user_moves = ...
            resp.message("Here's my first move! Good luck!\n" + valid_user_moves)
        elif body == "White":
            # Get valid user moves from stockfish from the starting board
            valid_user_moves = ...
            resp.message("Your move first! Good luck!\n" + valid_user_moves)
            
            
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