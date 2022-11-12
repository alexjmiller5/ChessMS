import os
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

# imported local files
import chess_manager as cm
import fen_parser as fp
import query as q

# account_sid = 'ACe0a977fae42fe85c925bb4bd3eeaf0f1' # replace later with os.environ[]
# auth_token = '91348d25f4044be9d69bdd9c2ed3db9a' # replace later with os.environ[]
# client = Client(account_sid, auth_token)

STARTING_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # starting chess board

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])

def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None) 
    user_phone = request.values.get('from', None)

    # Start our TwiML response
    resp = MessagingResponse() 

    # check database to see if client has been here before
    if q.check_user_exists == False:
        q.create_user(user_phone)
    
    if body == "Let's play chess!":
        resp.message("Black or White?")
        q.update_board(user_phone, "Game Initiated")

    user_board = q.get_board_for(user_phone)

    if user_board == "Game Initiated":
        if body == "Black":
            resp.message("Easy, medium, or hard difficulty?")
            q.update_board(user_phone, "Game Initiated Black")
        elif body == "White":
            resp.message("Easy, medium, or hard difficulty?")
            q.update_board(user_phone, "Game Initiated White")
        else:
            resp.message("Please choose a valid color")
    elif user_board == "Game Initiated Black":
            valid_user_moves = cm.get_legal_moves(new_user_board)
            new_user_board = STARTING_BOARD
            q.update_board(user_phone, new_user_board)
            new_user_board = fp.fen_to_ascii(new_user_board)

            resp.message("Your move first! Good luck!\n" + new_user_board + "\nValid Moves:" + valid_user_moves)
    elif user_board == "Game Initiated White":
            new_user_board = STARTING_BOARD
            new_user_board = cm.make_ai_move(new_user_board)
            q.update_board(user_phone, new_user_board)

            new_user_board = fen_to_ascii(new_user_board)
            valid_user_moves = cm.get_legal_moves(new_user_board)

            resp.message("Here's my first move! Good luck!\n" + new_user_board + "\nValid Moves:" + valid_user_moves)
    elif user_board != "":
        user_move = body
        prev_valid_moves = cm.get_legal_moves(user_board)
        if user_move in prev_valid_moves:
            user_moved_board = cm.make_user_move(user_board, user_move)
            if cm.is_checkmate(user_moved_board) == True:
                num_wins = q.get_win(user_phone) + 1
                q.update_board(user_phone, "")
                q.update_draw(user_phone, num_wins)
                resp.message("Congradulations! You won! You have {num_wins} wins total".format)
            elif cm.is_stalemate(user_moved_board) == True:
                num_draws = q.get_draw(user_phone) + 1
                q.update_board(user_phone, "")
                q.update_draw(user_phone, num_draws)
                resp.message("Oh no! A stalemate has been reached. You have {num_draws} total".format)
            else:
                new_user_board = cm.make_ai_move(user_moved_board)
                if cm.is_checkmate(new_user_board) == True:
                    num_losses = q.get_loss(user_phone) + 1
                    q.update_board(user_phone, "")
                    q.update_loss(user_phone, num_losses)
                    resp.message("Oh no! You lost. You have {num_losses} losses total".format)
                elif cm.is_stalemate(new_user_board) == True:
                    num_draws = q.get_draw(user_phone) + 1
                    q.update_board(user_phone, "")
                    q.update_draw(user_phone, num_draws)
                    resp.message("Oh no! A stalemate has been reached. You have {num_draws} total".format)
                else: 
                    q.update_board(user_phone, new_user_board)
                    new_user_board = fp.fen_to_ascii(new_user_board)
                    valid_next_moves = cm.get_legal_moves(new_user_board)
                    if cm.is_check(new_user_board) == True:
                        resp.message(new_user_board + "\nYou're in Check!\nValid Moves:" + valid_next_moves)
                    else:
                        resp.message(new_user_board + "\nValid Moves:" + valid_next_moves)
        else:
            resp.message("Invalid move, please send a valid move")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)