import pygame
import sys
from checkers.constants import *
from checkers.game import Game
from checkers.ai import minimax, minimax_with_alpha_beta, minimax_with_forward_pruning

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_win_window(winner):
    pygame.font.init()
    font = pygame.font.Font('assets/BELL.TTF', 40)
    WIN.blit(DARK_RED, DARK_RED.get_rect())
    text = font.render(f'{winner} won!', True, GOLD)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 4, HEIGHT//4)
    WIN.blit(text, text_rect)

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
    text_rect.center = (WIDTH // 4, HEIGHT//8)
    WIN.blit(text, text_rect)
    font = pygame.font.Font('assets/BELL.TTF', 24)
    options = ["Player VS. Player", "Player VS. AI", "AI VS. AI"]
    button_width, button_height = 200, 50

    buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect((WIDTH//2 - button_width) // 2, (HEIGHT//2 + i * 60) - (4 - i)*20 - (button_height // 2),
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


def start(mode=0):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    while run:
        clock.tick(FPS)
        game.update()
        if game.winner() is not None:
            print(game.winner(), " Winner")
            display_win_window(game.winner())
            pygame.quit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            
            if mode != AI_VS_AI:
                if game.turn == WHITE and mode == PLAYER_VS_AI:
                    value, new_board = minimax(game.get_board(), 4, WHITE, game)
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

                if game.turn == WHITE:
                    value, new_board_white = minimax_with_alpha_beta(game.get_board(), 4, float('-inf'), float('inf'), False, game)
                    print(value, new_board_white)
                    if value == 'False':
                        return
                    game.ai_move(new_board_white)
                    clock.tick(FPS)
                
                if game.turn == BLACK:
                    value, new_board_black = minimax_with_alpha_beta(game.get_board(), 4, float('-inf'), float('inf'), True, game)
                    print(value, new_board_black)
                    if value == 'False':
                        return
                    game.ai_move(new_board_black)
                    clock.tick(FPS)


        game.update()
    pygame.quit()

if __name__  == '__main__':
    pygame.init()
    pygame.font.init()

    while True:
        FPS = 60
        WIN = pygame.display.set_mode((WIDTH//2, HEIGHT))
        pygame.display.set_caption('Checkers')
        icon = pygame.transform.scale(ICON, ICON_SIZE)
        pygame.display.set_icon(icon)
        mode = display_options()
        if mode == PLAYER_VS_PLAYER:
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            start(mode=PLAYER_VS_PLAYER)

        elif mode == PLAYER_VS_AI:
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            start(mode=PLAYER_VS_AI)

        elif mode == AI_VS_AI:
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            start(mode=AI_VS_AI)
            break
