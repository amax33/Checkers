import pygame

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
ICON_SIZE = (64, 64)

# rgb
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 250, 250)
BLACK = (0, 0, 0)
BROWN = (150, 50, 0)
BEIGE = (255, 220, 150)
GOLD = (255, 230, 0)
DARK_GOLD = (252, 194, 0)
GRAY = (150, 150, 150)

CROWN_WHITE = pygame.transform.scale(pygame.image.load('assets/GOLDKING.png'), (SQUARE_SIZE * 2 // 3, SQUARE_SIZE * 2 // 3))
CROWN_BLACK = pygame.transform.scale(pygame.image.load('assets/BLACKKING.png'), (SQUARE_SIZE * 2 // 3, SQUARE_SIZE * 2 // 3))
DARK_RED = pygame.transform.scale(pygame.image.load('assets/dark_red.jpg'), (WIDTH//2, HEIGHT))
ICON = pygame.transform.scale(pygame.image.load('assets/ICON.png'), (WIDTH//2, HEIGHT))




PLAYER_VS_PLAYER = 0
PLAYER_VS_AI = 1
AI_VS_AI = 2

EASY = 1
NORMAL = 3
HARD = 5

