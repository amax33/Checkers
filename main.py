import pygame
import sys
import os
from checkers.constants import *
from checkers.game import Game
from checkers.ai import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def display_win_window(winner):
    WIN = pygame.display.set_mode((WIDTH * 2 // 3, HEIGHT // 3))
    pygame.font.init()
    font = pygame.font.Font('assets/BELL.TTF', 40)
    WIN.blit(pygame.transform.rotate(DARK_RED, 90), pygame.transform.rotate(DARK_RED, 90).get_rect())
    if winner == (255, 250, 250):
        text = font.render('Player White won!', True, GOLD)
    elif winner == (0, 0, 0):
        text = font.render('Player Black won!', True, GOLD)
    else:
        text = font.render('Draw!!!', True, GOLD)

    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 3, HEIGHT // 6)
    WIN.blit(text, text_rect)
    pygame.display.flip()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return -1


def display_options():
    pygame.font.init()
    font = pygame.font.Font('assets/BELL.TTF', 40)
    WIN.blit(DARK_RED, DARK_RED.get_rect())
    text = font.render('CHECKERS', True, GOLD)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 4, HEIGHT // 8)
    WIN.blit(text, text_rect)
    font = pygame.font.Font('assets/BELL.TTF', 24)
    options = ["Player VS. Player", "Player VS. AI", "AI VS. AI"]
    button_width, button_height = 200, 50

    buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect((WIDTH // 2 - button_width) // 2,
                                  (HEIGHT // 2 + i * 60) - (4 - i) *
                                  20 - (button_height // 2),
                                  button_width, button_height)
        buttons.append(button_rect)

    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Option selected: {options[i]}")
                        return i

        for i, button in enumerate(buttons):
            pygame.draw.rect(WIN, BEIGE if button.collidepoint(mouse_pos) else GOLD,
                             button)  # Change color if mouse over
            text = font.render(options[i], True, BLACK)
            text_rect = text.get_rect(center=button.center)
            WIN.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(30)
    return -1


def level_options(color):
    WIN = pygame.display.set_mode((WIDTH // 2, HEIGHT // 2))
    pygame.font.init()
    font = pygame.font.Font('assets/BELL.TTF', 15)
    WIN.blit(DARK_RED, DARK_RED.get_rect())
    text = font.render('Choose level of hardness of ' +
                       color + ' Player', True, GOLD)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 4, HEIGHT // 8)
    WIN.blit(text, text_rect)
    font = pygame.font.Font('assets/BELL.TTF', 15)
    options = ["Easy", "Normal", "Hard"]
    button_width, button_height = 150, 30

    buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect((WIDTH // 2 - button_width) // 2,
                                  (HEIGHT // 3 + i * 40) - (4 - i) *
                                  20 - (button_height // 2),
                                  button_width, button_height)
        buttons.append(button_rect)

    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Option selected: {options[i]}")
                        return i

        for i, button in enumerate(buttons):
            pygame.draw.rect(WIN, BEIGE if button.collidepoint(mouse_pos) else GOLD,
                             button)  # Change color if mouse over
            text = font.render(options[i], True, BLACK)
            text_rect = text.get_rect(center=button.center)
            WIN.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(30)
    return -1


def start(mode=0, levelW=0, levelB=0):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    round_counter = 0
    board_condition = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    while run:
        clock.tick(FPS)
        game.update()
        stuck_flag = None
        if game.winner() is not None:
            display_win_window(game.winner())
            pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if mode != AI_VS_AI:
                if game.turn == WHITE and mode == PLAYER_VS_AI:
                    value, new_board = minimax_alpha_beta(
                        game.get_board(), levelW, False, game, stuck_flag)
                    game.ai_move(new_board)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)

                    if game.turn == BLACK:
                        game.select(row, col)

                    elif game.turn == WHITE and mode == PLAYER_VS_PLAYER:
                        game.select(row, col)

            else:
                game.update()
                pygame.event.pump()
                board = game.get_board()
                for b in board_condition:
                    if [] not in board_condition:
                        if compare(b, board):
                            stuck_flag = board_condition[(round_counter - 1) % 16]
                board_condition[round_counter % 16] = board
                if game.turn == WHITE:
                    value, new_board_white = minimax_alpha_beta(game.get_board(), levelW, False, game, stuck_flag, prune=True)
                    game.ai_move(new_board_white)

                if game.turn == BLACK:
                    value, new_board_black = minimax_alpha_beta(game.get_board(), levelB, True, game, stuck_flag, prune=True)
                    game.ai_move(new_board_black)
                round_counter += 1

        game.update()
    pygame.quit()


def compare(b1, b2):
    board1 = b1.get_board_list()
    board2 = b2.get_board_list()
    for i in range(len(board1)):
        if board1[i] == 0 and board2[i] != 0:
            return False
        if board1[i] == (0, 0, 0) and board2[i] != (0, 0, 0):
            return False
        if board1[i] == (255, 250, 250) and board2[i] != (255, 250, 250):
            return False
    return True


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    hardness = {0: EASY, 1: NORMAL, 2: HARD}

    while True:
        FPS = 29
        WIN = pygame.display.set_mode((WIDTH // 2, HEIGHT))
        pygame.display.set_caption('Checkers')
        icon = pygame.transform.scale(ICON, ICON_SIZE)
        pygame.display.set_icon(icon)
        mode = display_options()
        if mode == PLAYER_VS_PLAYER:
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            start(mode=PLAYER_VS_PLAYER)

        elif mode == PLAYER_VS_AI:
            levelw = hardness.get(level_options('AI'))
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            start(mode=PLAYER_VS_AI, levelW=levelw)

        elif mode == AI_VS_AI:
            levelw = hardness.get(level_options('White'))
            levelb = hardness.get(level_options('Black'))
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            start(mode=AI_VS_AI, levelW=levelw, levelB=levelb)
