import pygame.draw

from .constants import BLACK, WHITE, SQUARE_SIZE, CROWN_BLACK, CROWN_WHITE


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False


        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), SQUARE_SIZE * 2 // 5)
        if self.king:
            if self.color == WHITE:
                win.blit(CROWN_BLACK, (self.x - CROWN_BLACK.get_width() // 2, self.y - CROWN_BLACK.get_height() // 2))
            else:
                win.blit(CROWN_WHITE, (self.x - CROWN_WHITE.get_width() // 2, self.y - CROWN_WHITE.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
