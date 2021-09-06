
class Game:
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
