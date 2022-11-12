# https://github.com/zhelyabuzhsky/stockfish

from stockfish import Stockfish, StockfishException
import fen_parser
from enum import Enum
from typing import List
import chess
from chess import Move

STARTING_BOARD = chess.STARTING_FEN

# TODO stockfish parameters, e.g. depth, threads, ELO rating

# TODO use 'chess.Move' object to translate between stockfish format and standard format

Fen = str  # Chessboard state

sf = Stockfish()

class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class InvalidMove(Exception):
    move: str
class InvalidState(Exception):
    state: Fen


def make_user_move(state:Fen, move:str) -> Fen:
    if not sf.is_fen_valid(state):
        raise InvalidState(state)
    if not sf.is_move_correct(move):
        raise InvalidMove(move)
    
    sf.set_fen_position(state)
    sf.make_moves_from_current_position([move])
    return sf.get_fen_position()


def make_ai_move(state:Fen, diff:Difficulty) -> Fen:
    sf.set_fen_position(state)
    move = sf.get_best_move()

    if move == None:
        raise StockfishException()
    
    sf.make_moves_from_current_position([move])
    return sf.get_fen_position()



def sf_to_obj(sf:str) -> Move:
    from_square = chess.parse_square(sf[:2])
    to_square   = chess.parse_square(sf[2:])
    return Move(from_square, to_square)

def obj_to_sf(obj:Move) -> str:
    from_square = chess.square_name(obj.from_square)
    to_square   = chess.square_name(obj.to_square)
    return from_square + to_square



def get_legal_moves(state:Fen) -> List[str]:
    moves = list(chess.Board(fen=state).legal_moves)
    return list(map(obj_to_sf, moves))



def is_check(state:Fen):
    return chess.Board(fen=state).is_check()

def is_checkmate(state:Fen):
    return chess.Board(fen=state).is_checkmate()

def is_stalemate(state:Fen):
    return chess.Board(fen=state).is_stalemate()


if __name__ == '__main__':
    #b = chess.Board(fen=STARTING_BOARD)
    print(get_legal_moves(STARTING_BOARD))
    #make_user_move(STARTING_BOARD, 'b5c6')

    #state = STARTING_BOARD
    #print(fen_parser.fen_to_ascii(state) + '\n')
    #state,_ = make_user_move(state, 'e2e4')
    #print(fen_parser.fen_to_ascii(state) + '\n')
    #state,_ = make_ai_move(state)
    #print(fen_parser.fen_to_ascii(state) + '\n')