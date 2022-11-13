# https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
# Convert FEN string to text

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import parse
from chess import Color, PieceType
import chess, chess.svg


Piece = Tuple[Color, PieceType]
Square = Optional[Piece]
Rank = Tuple[Square,Square,Square,Square,Square,Square,Square,Square]
Board = Tuple[Rank,Rank,Rank,Rank,Rank,Rank,Rank,Rank]


fen_parse = parse.compile(
    '{b[0]}/{b[1]}/{b[2]}/{b[3]}/{b[4]}/{b[5]}/{b[6]}/{b[7]} {turn} {castling} {passant} {halfmove} {fullmove}'
)

piece_fens = {v:k for k,v in enumerate(chess.PIECE_SYMBOLS)}

def fen_to_piece(fen:str) -> Piece:
    lower = fen.lower()
    piece_type = piece_fens[lower]
    color = chess.BLACK if fen == lower else chess.WHITE
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


BLANK = '-'

def square_to_ascii(sq:Square) -> str:
    if sq == None:
        return BLANK
    
    color, piece = sq
    s = chess.PIECE_SYMBOLS[piece]
    if color == chess.WHITE:
        s = s.upper()
    return s

def rank_to_ascii(rank:Rank) -> str:
    return ' '.join(map(square_to_ascii, rank))

def board_to_ascii(board:Board) -> str:
    return '\n'.join(map(rank_to_ascii, board))


def fen_to_ascii(fen:str) -> str:
    return board_to_ascii(fen_to_board(fen))

def char_to_unicode(c:str) -> str:
    if c == 'p':
        return '▲'
    if c in chess.UNICODE_PIECE_SYMBOLS:
        return chess.UNICODE_PIECE_SYMBOLS[c]
    elif c == BLANK:
        return '-'
    else: 
        return c

def fen_to_unicode(fen:str) -> str:
    s = fen_to_ascii(fen)
    return ''.join(map(char_to_unicode, s))

def boxify(s:str) -> str:
    ss = s.splitlines()
    l = len(ss[0])
    ss = [str(8-i) + '│' + s + '│' for i,s in enumerate(ss)]
    files = '  a b c d e f g h  '
    top = ' ┌' + '─' * l + '┐'
    bot = ' └' + '─' * l + '┘'

    return files + '\n' + top + '\n' + '\n'.join(ss) + '\n' + bot

def fen_to_boxed_unicode(fen:str) -> str:
    return boxify(fen_to_unicode(fen))
    
def fen_to_boxed_ascii(fen:str) -> str:
    return boxify(fen_to_ascii(fen))

def fen_to_svg(fen:str) -> str:
    b = chess.Board(fen=fen)
    return chess.svg.board(b)

def fen_to_svg_file(fen:str, path:str) -> None:
    svg = fen_to_svg(fen)
    with open(path, 'w') as fo:
        fo.write(svg)

if __name__ == '__main__':
    print(fen_to_unicode('1nbqkbnr/rpNppppp/p7/3P4/Q1P1PB2/5N2/PP2BPPP/R3K2R b KQk - 0 11'))
    # print(fen_to_ascii('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'))
    # print()
    # print(fen_to_unicode('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'))
    # print()
    # print(fen_to_boxed_unicode('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'))
    # print()
    # print(fen_to_boxed_ascii('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'))