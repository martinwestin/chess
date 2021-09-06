import pygame
import board
import os
import game


pygame.font.init()
WHITE_KING_SPRITE = pygame.image.load(os.path.join("sprites", "w_k.png"))
BLACK_KING_SPRITE = pygame.image.load(os.path.join("sprites", "b_k.png"))
WHITE_QUEEN_SPRITE = pygame.image.load(os.path.join("sprites", "w_q.png"))
BLACK_QUEEN_SPRITE = pygame.image.load(os.path.join("sprites", "b_q.png"))
WHITE_ROOK_SPRITE = pygame.image.load(os.path.join("sprites", "w_r.png"))
BLACK_ROOK_SPRITE = pygame.image.load(os.path.join("sprites", "b_r.png"))
WHITE_KNIGHT_SPRITE = pygame.image.load(os.path.join("sprites", "w_n.png"))
BLACK_KNIGHT_SPRITE = pygame.image.load(os.path.join("sprites", "b_n.png"))
WHITE_BISHOP_SPRITE = pygame.image.load(os.path.join("sprites", "w_b.png"))
BLACK_BISHOP_SPRITE = pygame.image.load(os.path.join("sprites", "b_b.png"))
WHITE_PAWN_SPRITE = pygame.image.load(os.path.join("sprites", "w_p.png"))
BLACK_PAWN_SPRITE = pygame.image.load(os.path.join("sprites", "b_p.png"))

sprite_map = {"w_k": WHITE_KING_SPRITE, "b_k": BLACK_KING_SPRITE, "w_q": WHITE_QUEEN_SPRITE, "b_q": BLACK_QUEEN_SPRITE,
              "w_r": WHITE_ROOK_SPRITE, "b_r": BLACK_ROOK_SPRITE, "w_n": WHITE_KNIGHT_SPRITE,
              "b_n": BLACK_KNIGHT_SPRITE, "w_b": WHITE_BISHOP_SPRITE, "b_b": BLACK_BISHOP_SPRITE,
              "w_p": WHITE_PAWN_SPRITE, "b_p": BLACK_PAWN_SPRITE}


class ChessApp:
    def __init__(self):
        self.rects = []
        self.WIDTH, self.HEIGHT = 700, 700
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")
        self.FPS = 60
        self.run = True
        self.board = board.Board(self.WIDTH, self.HEIGHT)
        self.font = pygame.font.SysFont("Arial", 20)

        self.lost = False

    def draw_window(self):
        self.WIN.fill((255, 255, 255))
        pygame.draw.rect(self.WIN, (0, 0, 0), self.board, 5)
        turn = "WHITE" if self.board.game.current_turn == "w" else "BLACK"
        if not self.lost:
            self.WIN.blit(self.font.render(f"{turn}'S TURN", True, (0, 0, 0)), (100, 50))
        else:
            self.WIN.blit(self.font.render(f"{turn} WAS CHECKMATED", True, (0, 0, 0)), (100, 50))

        for square in self.board.squares:
            pygame.draw.rect(self.WIN, square.color, square)

            if square.has_piece:
                self.WIN.blit(sprite_map[str(square.piece)], (square.x + 5, square.y + 5))
        piece_in_check = self.board.piece_in_check()
        if piece_in_check is not None:
            check_square = list(filter(lambda x: x.piece == piece_in_check, self.board.squares))[0]
            pygame.draw.rect(self.WIN, (255, 0, 0), check_square, 5)

        pygame.display.update()

    def run_app(self):
        clock = pygame.time.Clock()
        while self.run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN and not self.lost:
                    px, py = pygame.mouse.get_pos()
                    for square in self.board.squares:
                        end_x = square.x + square.width
                        end_y = square.y + square.height
                        if square.x <= px < end_x and square.y <= py < end_y:
                            self.board.select_square(square)
                if event.type == game.Game.CHECKMATE_EVENT:
                    self.lost = True

            self.draw_window()


if __name__ == '__main__':
    app = ChessApp()
    app.run_app()
