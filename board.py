import pygame
import chess_piece
import game
from typing import List


class Square(pygame.Rect):
    DARK_COLOR = (13, 79, 97)
    LIGHT_COLOR = (216, 225, 227)
    OFFSET_X = 100
    OFFSET_Y = 100

    def __init__(self, x: int,
                 y: int,
                 color: tuple,
                 piece: chess_piece.Piece,
                 width: float = 62.5,
                 height: float = 62.5,
                 ):
        super(Square, self).__init__(x * width + self.OFFSET_X, y * height + self.OFFSET_Y, width, height)
        self.col = x
        self.row = y
        self.row = list(reversed(range(8))).index(self.row)
        self.index = self.row * 8 + self.col
        self.color = color
        self.piece = piece

    def place_piece(self, piece: chess_piece.Piece):
        self.piece = piece

    def un_place(self):
        self.piece = None

    @property
    def has_piece(self):
        return self.piece is not None


class Board(pygame.Rect):
    MOVEMENT_TRACK_PIECES = [chess_piece.Pawn, chess_piece.King, chess_piece.Rook]

    def __init__(self, s_width: int, s_height: int):
        super(Board, self).__init__(s_width - (s_width - 100), s_height - (s_height - 100), 500, 500)
        self.squares = []
        self.reset_squares()

        self.selected_square = None
        self.SELECT_COLOR = (255, 80, 80)
        self.game = game.Game()
        self.starting_pos()

    def reset_squares(self):
        self.squares.clear()
        for row in reversed(range(8)):
            for col in range(8):
                color = Square.LIGHT_COLOR if (row + col) % 2 == 0 else Square.DARK_COLOR
                self.squares.append(Square(col, row, color, None))

    def select_square(self, square: Square):
        if self.selected_square is not None:
            if self.selected_square.has_piece:
                if self.selected_square.piece.color == self.game.current_turn:
                    if square != self.selected_square:
                        if self.selected_square.piece.move_was_legal(square, self.squares):
                            try:
                                self.move_piece(self.selected_square.piece, square)
                            except game.InCheckError:
                                pass

            self.selected_square.color = Square.LIGHT_COLOR if \
                (self.selected_square.row + self.selected_square.col) % 2 != 0 else Square.DARK_COLOR

        self.selected_square = square
        self.selected_square.color = self.SELECT_COLOR

    def check_scan(self, piece: chess_piece.Piece, from_square: Square, to_square: Square):
        """
        Check if last move was illegal. If it was, undo it and raise InCheckError.
        :param piece: the piece that is moving.
        :param from_square: from what square the piece is moving.
        :param to_square: to what square the piece is moving.
        :return:
        """
        piece_in_check = self.piece_in_check(self.squares)
        if piece_in_check is not None:
            if self.game.current_turn == piece_in_check.color:
                # last move must have been illegal since the king is still in check, undo last move
                last_move = self.game.last_move
                self.game.undo_latest_move()
                to_square.un_place()
                self.squares[self.squares.index(from_square)].place_piece(piece)
                piece.move(last_move[1].index)
                raise game.InCheckError("Move is illegal as it places the king in check.")

    def move_piece(self, piece: chess_piece.Piece, to_square: Square, check_scan: bool = True):
        from_square = list(filter(lambda x: x.piece == piece, self.squares))[0]
        col, row = piece.get_col_row(self.squares)

        to_square.place_piece(piece)
        from_square.un_place()
        piece.move(to_square.index)
        self.game.add_move(piece, self.squares[self.squares.index(from_square)], to_square)
        if check_scan:
            self.check_scan(piece, from_square, to_square)

        if type(piece) in self.MOVEMENT_TRACK_PIECES:
            piece.moved()

            if type(piece) == chess_piece.Pawn:
                if not piece.has_moved:
                    piece.moved()
                if row == 7 or row == 0:
                    self.squares[piece.index].place_piece(chess_piece.Queen(piece.index, piece.color))

        self.game.next_turn()
        possible_moves = self.possible_moves(self.game.current_turn, self.squares)
        if len(possible_moves) == 0:
            pygame.event.post(pygame.event.Event(self.game.CHECKMATE_EVENT))

    def starting_pos(self):
        # white pieces
        self.squares[4].place_piece(chess_piece.King(4, "w"))
        self.squares[3].place_piece(chess_piece.Queen(3, "w"))
        self.squares[0].place_piece(chess_piece.Rook(0, "w"))
        self.squares[7].place_piece(chess_piece.Rook(7, "w"))
        self.squares[1].place_piece(chess_piece.Knight(1, "w"))
        self.squares[6].place_piece(chess_piece.Knight(6, "w"))
        self.squares[2].place_piece(chess_piece.Bishop(2, "w"))
        self.squares[5].place_piece(chess_piece.Bishop(5, "w"))

        for i in range(8, 16):
            self.squares[i].place_piece(chess_piece.Pawn(i, "w"))

        # black_pieces
        self.squares[60].place_piece(chess_piece.King(60, "b"))
        self.squares[59].place_piece(chess_piece.Queen(59, "b"))
        self.squares[63].place_piece(chess_piece.Rook(63, "b"))
        self.squares[56].place_piece(chess_piece.Rook(56, "b"))
        self.squares[57].place_piece(chess_piece.Knight(57, "b"))
        self.squares[62].place_piece(chess_piece.Knight(62, "b"))
        self.squares[58].place_piece(chess_piece.Bishop(58, "b"))
        self.squares[61].place_piece(chess_piece.Bishop(61, "b"))

        for i in range(48, 56):
            self.squares[i].place_piece(chess_piece.Pawn(i, "b"))

    def piece_in_check(self, squares: List[Square]):
        king_squares = list(filter(lambda x: type(x.piece) == chess_piece.King, squares))

        for square in list(filter(lambda x: x not in king_squares, self.piece_squares(squares))):
            piece = square.piece
            for k_s in king_squares:
                if type(piece) != chess_piece.Pawn:
                    legal = piece.move_was_legal(k_s, squares)
                else:
                    legal = piece.legal_take(k_s, squares)
                if legal:
                    return k_s.piece

    def possible_moves(self, color: str, squares: List[Square]):
        piece_squares = self.piece_squares(squares)
        piece_squares = list(filter(lambda x: x.piece.color == color, piece_squares))
        pieces = list(map(lambda x: x.piece, piece_squares))
        ignore_squares = list(filter(lambda x: x.piece.color == color, self.piece_squares(squares)))
        to_check = list(filter(lambda x: x not in ignore_squares, squares))

        possible_outcomes = []
        for piece in pieces:
            for square in to_check:
                square_piece = square.piece

                if piece.move_was_legal(square, squares):
                    # o_s ==> original square the piece moved from
                    o_s = list(filter(lambda x: x.index == piece.index, squares))[0]
                    o_s.un_place()
                    square.place_piece(piece)
                    piece_in_check = self.piece_in_check(squares)
                    if piece_in_check is not None:
                        piece_in_check = None if piece_in_check.color != piece.color else piece_in_check

                    if piece_in_check is None:
                        # (current_state, (piece to move, square to move to))
                        square_copy = [Square(s.col, s.row, s.color, s.piece) for s in squares]
                        possible_outcomes.append((square_copy, (piece, square)))

                    square.un_place()
                    if square_piece is not None:
                        square.place_piece(square_piece)

                    o_s.place_piece(piece)

        return possible_outcomes

    def fetch_square_by_index(self, index: int):
        return list(filter(lambda square: square.index == index, self.squares))[0]

    def leading(self):
        w_sum, b_sum = 0, 0
        for square in self.piece_squares(self.squares):
            if type(square.piece) != chess_piece.King:
                value = square.piece.value
                if square.piece.color == "w":
                    w_sum += value
                else:
                    b_sum += value

        if w_sum != b_sum:
            if w_sum > b_sum:
                return "w", int(w_sum / 100 - b_sum / 100)
            return "b", int(b_sum / 100 - w_sum / 100)

    @staticmethod
    def piece_squares(squares: List[Square]):
        return list(filter(lambda x: x.has_piece, squares))
