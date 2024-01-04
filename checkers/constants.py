import pygame

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 250, 250)
BLACK = (0, 0, 0)
BROWN = (150, 50, 0)
BEIGE = (255, 220, 150)

CROWN_WHITE = pygame.transform.scale(pygame.image.load('assets/WHITEKING.png'), (SQUARE_SIZE * 2 // 3, SQUARE_SIZE * 2 // 3))
CROWN_BLACK = pygame.transform.scale(pygame.image.load('assets/BLACKKING.png'), (SQUARE_SIZE * 2 // 3, SQUARE_SIZE * 2 // 3))
