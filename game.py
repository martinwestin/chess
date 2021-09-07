import pygame
import chess_piece


class InCheckError(Exception):
    pass


class Game:
    CHECKMATE_EVENT = pygame.USEREVENT + 1

    def __init__(self):
        self.turn = "w"
        self.moves = []

    def next_turn(self):
        self.turn = "b" if self.turn == "w" else "w"

    @property
    def current_turn(self):
        return self.turn

    def add_move(self, piece, from_square, to_square):
        self.moves.append((piece, from_square, to_square))

    def undo_latest_move(self):
        self.moves.remove(self.moves[-1])

    @property
    def last_move(self):
        return self.moves[-1]

    @staticmethod
    def evaluation(squares: list, color: str = "b"):
        piece_squares = list(filter(lambda x: x.has_piece, squares))
        pieces = list(map(lambda x: x.piece, list(filter(lambda x: x.piece.color == color, piece_squares))))
        evaluation = sum([piece.value for piece in pieces if type(piece) != chess_piece.King])

        return evaluation
