# https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
# Convert FEN string to text

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import parse

class Color(Enum):
    BLACK = 0
    WHITE = 1

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


Piece = Tuple[Color, PieceType]
Square = Optional[Piece]
Rank = Tuple[Square,Square,Square,Square,Square,Square,Square,Square]
Board = Tuple[Rank,Rank,Rank,Rank,Rank,Rank,Rank,Rank]


#@dataclass(frozen=True)
#class FEN:
#    ranks: List[str]
#    white_to_move: bool
#    castles: Tuple[bool,bool,bool,bool]
#    # 


fen_parse = parse.compile(
    '{b[0]}/{b[1]}/{b[2]}/{b[3]}/{b[4]}/{b[5]}/{b[6]}/{b[7]} {turn} {castling} {passant} {halfmove} {fullmove}'
)

fen_pieces = {
    PieceType.PAWN: 'p',
    PieceType.BISHOP: 'b',
    PieceType.KNIGHT: 'n',
    PieceType.QUEEN: 'q',
    PieceType.KING: 'k',
    PieceType.ROOK: 'r'
}

piece_fens = {v:k for k,v in fen_pieces.items()}

def fen_to_piece(fen:str) -> Piece:
    lower = fen.lower()
    piece_type = piece_fens[lower]
    color = Color.BLACK if fen == lower else Color.WHITE
    return (color, piece_type)

def fen_to_rank(fen:str) -> Rank:
    res = []
    for s in list(fen):
        if s.isdigit():
            res += [None] * int(s)
        elif s.isalpha():
            res.append(fen_to_piece(s))
        else:
            raise Exception()
    return tuple(res)
    

# https://github.com/r1chardj0n3s/parse
def fen_to_board(fen:str) -> Board:
    parsed = fen_parse.parse(fen, evaluate_result=True)

    if parsed == None or isinstance(parsed, parse.Match):
        raise Exception()

    pp = parsed.named
    b = pp['b']
    bb = [b[str(i)] for i in range(8)]
    
    return tuple(map(fen_to_rank, bb))


def square_to_ascii(sq:Square) -> str:
    if sq == None:
        return '-'
    
    color, piece = sq
    s = fen_pieces[piece]
    if color == Color.WHITE:
        s = s.upper()
    return s

def rank_to_ascii(rank:Rank) -> str:
    return ' '.join(map(square_to_ascii, rank))

def board_to_ascii(board:Board) -> str:
    return '\n'.join(map(rank_to_ascii, board))


def fen_to_ascii(fen:str) -> str:
    return board_to_ascii(fen_to_board(fen))

print(fen_to_ascii('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'))