# https://github.com/zhelyabuzhsky/stockfish

from stockfish import Stockfish
import fen_parser

# TODO stockfish parameters, e.g. depth, threads, ELO rating

Fen = str  # Chessboard state

sf = Stockfish()

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


if __name__ == '__main__':
    state = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    print(fen_parser.fen_to_ascii(state) + '\n')
    state = make_user_move(state, '...e5')
    print(fen_parser.fen_to_ascii(state) + '\n')