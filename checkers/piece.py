import pygame.draw
import pygame.gfxdraw
from pygame import Surface, SRCALPHA

from .constants import *


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
        radius = SQUARE_SIZE * 2 // 5
        center = pygame.math.Vector2(self.x, self.y)
        # To create the shadow, draw a darker circle a little bit offset from the piece
        if self.color == WHITE:
            pygame.draw.circle(win, self.color, (self.x, self.y), radius)
            if not self.king:
                # Calculate the position of the spark - this will be in the top left quadrant of the piece
                spark_x = self.x
                spark_y = self.y
                glow_surface = Surface((2 * (radius + 10), 2 * (radius + 10)), SRCALPHA)
                # Draw the spark
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 2 - 1, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 2, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 2 + 1, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 4, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius * 3 // 4, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius - 1, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius + 1, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y - 1, radius, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x + 1, spark_y, radius, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x - 1, spark_y, radius, BLACK)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y+1, radius, BLACK)  # Outer circle
                pygame.draw.ellipse(glow_surface, (255, 255, 255, 50), (0, 0, 2 * (radius + 10), 2 * (radius + 10)))
        if self.color == BLACK:
            pygame.draw.circle(win, self.color, (self.x, self.y), radius)
            if not self.king:
                # Calculate the position of the spark - this will be in the top left quadrant of the piece
                spark_x = self.x
                spark_y = self.y
                glow_surface = Surface((2 * (radius + 10), 2 * (radius + 10)), SRCALPHA)
                # Draw the spark
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 2 - 1, DARK_GOLD)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 2, DARK_GOLD)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 2 + 1, DARK_GOLD)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius // 4, DARK_GOLD)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius * 3 // 4, DARK_GOLD)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius - 1, DARK_GOLD)  # Outer circle
                pygame.gfxdraw.circle(win, spark_x, spark_y, radius, DARK_GOLD)  # Outer circle
                pygame.draw.circle(win, DARK_GOLD, (spark_x, spark_y), radius, width=3)  # Outer circle
                pygame.draw.ellipse(glow_surface, (255, 255, 255, 50), (0, 0, 2*(radius+10), 2*(radius+10)))

        # If the piece is a king, draw the crown
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
