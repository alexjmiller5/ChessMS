import os
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
# from flask_ngrok import run_with_ngrok

# imported local files
import chess_manager as cm
import fen_parser as fp
import database.query as q

# account_sid = 'ACe0a977fae42fe85c925bb4bd3eeaf0f1' # replace later with os.environ[]
# auth_token = '91348d25f4044be9d69bdd9c2ed3db9a' # replace later with os.environ[]
# client = Client(account_sid, auth_token)

STARTING_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # starting chess board

app = Flask(__name__)
# run_with_ngrok(app)

@app.route("/", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None) 
    body = body.lower()
    body = body.strip()
    user_phone = request.values.get('From', None)
    print(f"Message received: Body: {body} From: {user_phone}")

    # Start our TwiML response
    resp = MessagingResponse() 

    if user_phone == None:
        return

    # check database to see if client has been here before
    if q.check_user_exist(user_phone) == False:
        q.create_user(user_phone)
        print(f"Successfully created user in the database with phone {user_phone}")

    user_board = q.get_board_for(user_phone)
    print(f"Retrieved board \"{user_board}\" from the database from user \"{user_phone}\"")

    if body == "let's play chess!" or body == "let's play chess" or body == "lets play chess":
        resp.message("Black or White?")
        q.update_board(user_phone, "Game Initiated")

    elif user_board == "Game Initiated":
        if body == "black":
            resp.message("Easy, medium, or hard difficulty?")
            q.update_board(user_phone, "Game Initiated Black")
        elif body == "white":
            resp.message("Easy, medium, or hard difficulty?")
            q.update_board(user_phone, "Game Initiated White")
        else:
            resp.message("Please choose a valid color")

    elif user_board == "Game Initiated White":
        if body == "easy":
            q.update_difficulty_level(user_phone,0)
        if body == "medium":
            q.update_difficulty_level(user_phone,1)
        if body == "hard":
            q.update_difficulty_level(user_phone,2)
        if body == "easy" or body == "medium" or body == "hard":
            new_user_board = STARTING_BOARD
            q.update_board(user_phone, new_user_board)
            valid_user_moves = cm.get_legal_moves(new_user_board)
            new_user_board = fp.fen_to_unicode(new_user_board)
            valid_user_moves = ', '.join(valid_user_moves)
            resp.message("Your move first! Good luck!\n" + new_user_board + "\nValid Moves:\n" + valid_user_moves)

    elif user_board == "Game Initiated Black":
        if body == "easy":
            q.update_difficulty_level(user_phone,0)
        if body == "medium":
            q.update_difficulty_level(user_phone,1)
        if body == "hard":
            q.update_difficulty_level(user_phone,2)
        if body == "easy" or body == "medium" or body == "hard":
            new_user_board = STARTING_BOARD
            diff = q.get_difficulty_level_for(user_phone)
            new_user_board = cm.make_ai_move(new_user_board, diff)
            valid_user_moves = cm.get_legal_moves(new_user_board)
            q.update_board(user_phone, new_user_board)
            new_user_board = fp.fen_to_unicode(new_user_board)
            valid_user_moves = ', '.join(valid_user_moves)
            resp.message("Here's my first move! Good luck!\n" + new_user_board + "\nValid Moves:\n" + valid_user_moves)
        
    elif user_board != "":
        user_move = body
        prev_valid_moves = cm.get_legal_moves(user_board)

        if user_move in prev_valid_moves:
            user_moved_board = cm.make_user_move(user_board, user_move)

            if cm.is_checkmate(user_moved_board) == True:
                print("The user has won!")
                num_wins = q.get_win(user_phone) + 1
                q.update_board(user_phone, "")
                q.update_win(user_phone)
                resp.message(f'Congradulations! You won! You have {num_wins} wins total')

            elif cm.is_stalemate(user_moved_board) == True:
                print("A stalemate has been reached!")
                num_draws = q.get_draw(user_phone) + 1
                q.update_board(user_phone, "")
                q.update_draw(user_phone)
                resp.message(f'Oh no! A stalemate has been reached. You have {num_draws} total')

            else:
                diff = q.get_difficulty_level_for(user_phone)
                new_user_board = cm.make_ai_move(user_moved_board, diff)

                if cm.is_checkmate(new_user_board) == True:
                    print("The user has lost!")
                    num_losses = q.get_loss(user_phone) + 1
                    q.update_board(user_phone, "")
                    q.update_loss(user_phone)
                    resp.message(f'Oh no! You lost. You have {num_losses} losses total')

                elif cm.is_stalemate(new_user_board) == True:
                    print("A stalemate has been reached!")
                    num_draws = q.get_draw(user_phone) + 1
                    q.update_board(user_phone, "")
                    q.update_draw(user_phone)
                    resp.message(f'Oh no! A stalemate has been reached. You have {num_draws} total')

                else: 
                    q.update_board(user_phone, new_user_board)
                    valid_user_moves = cm.get_legal_moves(new_user_board)
                    valid_user_moves = ', '.join(valid_user_moves)
                    if cm.is_check(new_user_board) == True:
                        print("The user is in check!")
                        new_user_board = fp.fen_to_unicode(new_user_board)
                        resp.message("\n" + new_user_board + "\nYou're in Check!\nValid Moves:\n" + valid_user_moves)
                    
                    else:
                        print("The user is performing a standard move")
                        new_user_board = fp.fen_to_unicode(new_user_board)
                        resp.message("\n" + new_user_board + "\nValid Moves:\n" + valid_user_moves)
                        
        
        else:
            resp.message("Invalid move, please send a valid move")

    print("The outgoing message sent is " + str(resp))

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)