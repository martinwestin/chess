import game


class Piece:
    DIAGONAL_OFFSETS = [9, 7, -9, -7]
    VERTICAL_OFFSETS = [8, -8]
    HORIZONTAL_OFFSETS = [1, -1]

    def __init__(self, color: str, square_index: int):
        self.index = square_index
        self.color = color

    def moved_onto_teammate(self, to_square, squares: list):
        if squares[squares.index(to_square)].has_piece:
            square_piece = squares[squares.index(to_square)].piece
            return square_piece.color == self.color

    def piece_in_way(self, to_square, squares: list):
        current_square = list(filter(lambda x: x.piece == self, squares))[0]
        current_col, current_row = current_square.col, current_square.row
        to_col, to_row = to_square.col, to_square.row
        col_squares = list(filter(lambda x: x.col == current_col, squares))
        row_squares = list(filter(lambda x: x.row == current_row, squares))
        if current_col == to_col:
            if to_row > current_row:
                vertical = [col_square for col_square in col_squares if current_row < col_square.row < to_row]
            else:
                vertical = [col_square for col_square in col_squares if current_row > col_square.row > to_row]

            for square in vertical:
                if square.has_piece:
                    return True
        else:
            # check for horizontal and diagonal pieces in way
            if to_row == current_row:
                if to_col > current_col:
                    horizontal = [row_square for row_square in row_squares if current_col < row_square.col < to_col]
                else:
                    horizontal = [row_square for row_square in row_squares if current_col > row_square.col > to_col]

                for square in horizontal:
                    if square.has_piece:
                        return True
            else:
                index_diff = self.index - to_square.index
                if index_diff < 0:
                    # UP
                    square_indexes = [self.index + i * 9 for i in range(1, int(abs(index_diff) / 9))] \
                        if index_diff % 9 == 0 else [self.index + i * 7 for i in range(1, int(abs(index_diff) / 7))]
                    valid_squares = list(filter(lambda x: x.index in square_indexes, squares))
                    for d_s in valid_squares:
                        if d_s.has_piece:
                            return True
                else:
                    # DOWN
                    square_indexes = [self.index - i * 9 for i in reversed(range(1, int(abs(index_diff) / 9)))] \
                        if index_diff % 9 == 0 else \
                        [self.index - i * 7 for i in reversed(range(1, int(abs(index_diff) / 7)))]

                    valid_squares = list(filter(lambda x: x.index in square_indexes, squares))
                    for d_s in valid_squares:
                        if d_s.has_piece:
                            return True

    def get_col_row(self, squares: list):
        current_square = list(filter(lambda x: x.piece == self, squares))[0]
        return current_square.col, current_square.row

    def move(self, new_index: int):
        self.index = new_index

    def move_was_legal(self, to_square, squares: list) -> bool: ...


class King(Piece):
    def __init__(self, start_index: int, color: str):
        super(King, self).__init__(color, start_index)

    def __repr__(self):
        return "w_k" if self.color == "w" else "b_k"

    def move_was_legal(self, to_square, squares: list):
        if not self.moved_onto_teammate(to_square, squares):
            return self.index - to_square.index in self.HORIZONTAL_OFFSETS + self.VERTICAL_OFFSETS +\
                   self.DIAGONAL_OFFSETS


class Queen(Piece):
    def __init__(self, start_index: int, color: str):
        super(Queen, self).__init__(color, start_index)
        self.value = 900 if self.color == game.Game.AI_COLOR else -900

    def __repr__(self):
        return "w_q" if self.color == "w" else "b_q"

    def move_was_legal(self, to_square, squares: list):
        if not self.moved_onto_teammate(to_square, squares):
            current_square = list(filter(lambda x: x.piece == self, squares))[0]
            current_col, current_row = current_square.col, current_square.row
            to_col, to_row = to_square.col, to_square.row
            diagonal_squares = list(filter(lambda square: abs(to_col - current_col) == abs(to_square.row - current_row),
                                           squares))
            if not self.piece_in_way(to_square, squares):
                return current_col == to_col or current_row == to_row or to_square in diagonal_squares


class Rook(Piece):
    def __init__(self, start_index: int, color: str):
        super(Rook, self).__init__(color, start_index)
        self.value = 500 if self.color == game.Game.AI_COLOR else -500

    def __repr__(self):
        return "w_r" if self.color == "w" else "b_r"

    def move_was_legal(self, to_square, squares: list):
        if not self.moved_onto_teammate(to_square, squares):
            current_square = list(filter(lambda x: x.piece == self, squares))[0]
            current_col, current_row = current_square.col, current_square.row
            to_col, to_row = to_square.col, to_square.row
            if not self.piece_in_way(to_square, squares):
                return current_col == to_col or current_row == to_row


class Knight(Piece):
    def __init__(self, start_index: int, color: str):
        super(Knight, self).__init__(color, start_index)
        self.VALID_OFFSETS = [10, 6, 17, 15]
        self.value = 300 if self.color == game.Game.AI_COLOR else -300

    def __repr__(self):
        return "w_n" if self.color == "w" else "b_n"

    def move_was_legal(self, to_square, squares: list):
        return abs(self.index - to_square.index) in self.VALID_OFFSETS \
               and not self.moved_onto_teammate(to_square, squares)


class Bishop(Piece):
    def __init__(self, start_index: int, color: str):
        super(Bishop, self).__init__(color, start_index)
        self.value = 300 if self.color == game.Game.AI_COLOR else -300

    def __repr__(self):
        return "w_b" if self.color == "w" else "b_b"

    def move_was_legal(self, to_square, squares: list):
        if not self.moved_onto_teammate(to_square, squares):
            col, row = self.get_col_row(squares)
            valid_squares = list(filter(lambda square: abs(square.col - col) == abs(square.row - row), squares))
            if not self.piece_in_way(to_square, squares):
                return to_square in valid_squares


class Pawn(Piece):
    def __init__(self, start_index: int, color: str):
        super(Pawn, self).__init__(color, start_index)
        self.has_moved = False
        self.value = 100 if self.color == game.Game.AI_COLOR else -100

    def __repr__(self):
        return "w_p" if self.color == "w" else "b_p"

    def move_was_legal(self, to_square, squares: list):
        if not self.moved_onto_teammate(to_square, squares):
            current_square = list(filter(lambda x: x.piece == self, squares))[0]
            current_col, current_row = current_square.col, current_square.row
            to_col, to_row = to_square.col, to_square.row
            if to_row > current_row and self.color == "w" or to_row < current_row and self.color == "b":
                if abs(to_row - current_row) <= 2:
                    if not self.has_moved:

                        if abs(to_row - current_row) == 2 and to_col == current_col:
                            if not self.piece_in_way(to_square, squares):
                                return not to_square.has_piece
                        else:
                            if current_col == to_col:
                                return not to_square.has_piece
                            else:
                                if abs(current_col - to_col) == 1 and abs(to_row - current_row) != 2:
                                    return to_square.has_piece
                    else:
                        if abs(to_row - current_row) == 1:
                            if current_col == to_col:
                                return not to_square.has_piece
                            else:
                                if abs(current_col - to_col) == 1:
                                    return to_square.has_piece

    def legal_take(self, to_square, squares: list):
        current_col, current_row = self.get_col_row(squares)
        if not self.moved_onto_teammate(to_square, squares):
            if self.color == "w":
                return current_row + 1 == to_square.row and abs(current_col - to_square.col) == 1
            else:
                return current_row - 1 == to_square.row and abs(current_col - to_square.col) == 1

    def moved(self):
        self.has_moved = True
