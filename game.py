import pygame
import chess_piece


class InCheckError(Exception):
    pass


class Game:
    AI_COLOR = "b"
    CHECKMATE_EVENT = pygame.USEREVENT + 1
    AI_TURN_EVENT = pygame.USEREVENT + 2

    def __init__(self):
        self.turn = "w"
        self.moves = []

    def next_turn(self):
        self.turn = "b" if self.turn == "w" else "w"
        if self.turn == self.AI_COLOR:
            pygame.event.post(pygame.event.Event(self.AI_TURN_EVENT))

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
    def evaluation(squares: list):
        piece_squares = list(filter(lambda x: x.has_piece, squares))
        pieces = list(map(lambda x: x.piece, piece_squares))
        return sum(list(map(lambda piece: piece.value,
                            list(filter(lambda piece: type(piece) != chess_piece.King, pieces)))))
