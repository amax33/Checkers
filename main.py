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


# display the window when the game is won
def display_win_window(winner):
    # Create a new window with dimensions
    WIN = pygame.display.set_mode((WIDTH * 2 // 3, HEIGHT // 3))
    
    # Initialize the Pygame font module
    pygame.font.init()
    
    # Set the font for the window
    font = pygame.font.Font('assets/BELL.TTF', 40)
    
    # Draw a rotated DARK_RED background on the window
    WIN.blit(pygame.transform.rotate(DARK_RED, 90), pygame.transform.rotate(DARK_RED, 90).get_rect())
    
    # Check the winner and display corresponding text
    if winner == (255, 250, 250):
        text = font.render('Player White won!', True, GOLD)
    elif winner == (0, 0, 0):
        text = font.render('Player Black won!', True, GOLD)
    else:
        text = font.render('Draw!!!', True, GOLD)

    # Get the rectangle of the text and center it in the window
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 3, HEIGHT // 6)
    
    # Blit the text on the window
    WIN.blit(text, text_rect)
    
    # Update the display
    pygame.display.flip()

    # Enter a loop to wait for the user to close the window
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit Pygame and exit the program if the window is closed
                pygame.quit()
                sys.exit()

    return -1

# display the game mode options and handle user input
def display_options():
    # Initialize Pygame font module
    pygame.font.init()
    
    # Set the font for the window title
    font = pygame.font.Font('assets/BELL.TTF', 40)
    
    # Draw a background using the DARK_RED color
    WIN.blit(DARK_RED, DARK_RED.get_rect())
    
    # Render and center the 'CHECKERS' title text on the window
    text = font.render('CHECKERS', True, GOLD)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 4, HEIGHT // 8)
    WIN.blit(text, text_rect)
    
    # Change font size for options text
    font = pygame.font.Font('assets/BELL.TTF', 24)
    
    # List of game mode options
    options = ["Player VS. Player", "Player VS. AI", "AI VS. AI"]
    
    # Set dimensions for the option buttons
    button_width, button_height = 200, 50

    # Create Rect objects for each option button and store them in a list
    buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect((WIDTH // 2 - button_width) // 2,
                                  (HEIGHT // 2 + i * 60) - (4 - i) *
                                  20 - (button_height // 2),
                                  button_width, button_height)
        buttons.append(button_rect)

    # Enter a loop to wait for user input
    run = True
    while run:
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit Pygame and exit the program if the window is closed
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is inside any of the option buttons
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Option selected: {options[i]}")
                        return i  # Return the index of the selected option

        # Draw option buttons, change color if mouse is over, and display text
        for i, button in enumerate(buttons):
            pygame.draw.rect(WIN, BEIGE if button.collidepoint(mouse_pos) else GOLD,
                             button)  # Change color if mouse over
            text = font.render(options[i], True, BLACK)
            text_rect = text.get_rect(center=button.center)
            WIN.blit(text, text_rect)

        # Update the display and control the frame rate
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    return -1


#  display options for choosing the difficulty level of a player
def level_options(color):
    # Set up a Pygame window
    WIN = pygame.display.set_mode((WIDTH // 2, HEIGHT // 2))
    
    # Initialize Pygame font module
    pygame.font.init()
    
    # Set the font for the window title
    font = pygame.font.Font('assets/BELL.TTF', 15)
    
    # Draw a background using the DARK_RED color
    WIN.blit(DARK_RED, DARK_RED.get_rect())
    
    # Render and center the text indicating the purpose of the window
    text = font.render('Choose level of hardness of ' +
                       color + ' Player', True, GOLD)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 4, HEIGHT // 8)
    WIN.blit(text, text_rect)
    
    # Change font size for level options
    font = pygame.font.Font('assets/BELL.TTF', 15)
    
    # List of difficulty level options
    options = ["Easy", "Normal", "Hard"]
    
    # Set dimensions for the level buttons
    button_width, button_height = 150, 30

    # Create Rect objects for each level button and store them in a list
    buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect((WIDTH // 2 - button_width) // 2,
                                  (HEIGHT // 3 + i * 40) - (4 - i) *
                                  20 - (button_height // 2),
                                  button_width, button_height)
        buttons.append(button_rect)

    # Enter a loop to wait for user input
    run = True
    while run:
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit Pygame and exit the program if the window is closed
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is inside any of the level buttons
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Option selected: {options[i]}")
                        return i  # Return the index of the selected level

        # Draw level buttons, change color if mouse is over, and display text
        for i, button in enumerate(buttons):
            pygame.draw.rect(WIN, BEIGE if button.collidepoint(mouse_pos) else GOLD,
                             button)  # Change color if mouse over
            text = font.render(options[i], True, BLACK)
            text_rect = text.get_rect(center=button.center)
            WIN.blit(text, text_rect)

        # Update the display and control the frame rate
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    return -1

# start the game with specified mode and AI levels
def start(mode=0, levelW=0, levelB=0):
    # Initialize game variables
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    round_counter = 0
    # Store the board conditions for detecting repetitions
    board_condition = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    # Main game loop
    while run:
        # Control the frame rate
        clock.tick(FPS)
        
        game.update()
        
        # Check if there is a winner
        stuck_flag = None
        if game.winner() is not None:
            # Display the win window and quit the game
            display_win_window(game.winner())
            pygame.quit()

        # Check for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the window is closed
                run = False

            if mode != AI_VS_AI:
                # Player vs. AI mode logic
                if game.turn == WHITE and mode == PLAYER_VS_AI:
                    # AI's turn, use minimax with alpha-beta pruning to make a move
                    value, new_board = minimax_alpha_beta(
                        game.get_board(), levelW, False, game, stuck_flag)
                    game.ai_move(new_board)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Player's turn, handle mouse click events
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)

                    if game.turn == BLACK:
                        # Player vs. Player: Select a piece for the current player's turn
                        game.select(row, col)

                    elif game.turn == WHITE and mode == PLAYER_VS_PLAYER:
                        # Player vs. Player: Select a piece for the current player's turn
                        game.select(row, col)

            else:
                # AI vs. AI mode logic
                game.update()
                pygame.event.pump()
                board = game.get_board()
                
                # Detect repetitions to avoid an infinite loop
                for b in board_condition:
                    if [] not in board_condition:
                        if compare(b, board):
                            stuck_flag = board_condition[(round_counter - 1) % 16]
                
                board_condition[round_counter % 16] = board
                
                if game.turn == WHITE:
                    # White AI's turn, use minimax with alpha-beta pruning to make a move
                    value, new_board_white = minimax_alpha_beta(game.get_board(), levelW, False, game, stuck_flag, prune=False)
                    game.ai_move(new_board_white)

                if game.turn == BLACK:
                    # Black AI's turn, use minimax with alpha-beta pruning to make a move
                    value, new_board_black = minimax_alpha_beta(game.get_board(), levelB, True, game, stuck_flag, prune=False)
                    game.ai_move(new_board_black)
                
                round_counter += 1

        game.update()
    
    pygame.quit()

    
# Function to compare two board states for equality
def compare(b1, b2):
    # Extract board lists from the provided Game objects
    board1 = b1.get_board_list()
    board2 = b2.get_board_list()

    # Iterate through the board positions
    for i in range(len(board1)):
        # Check if the positions are not equal
        if board1[i] == 0 and board2[i] != 0:
            # Empty position in board1, but not in board2, not equal
            return False
        if board1[i] == (0, 0, 0) and board2[i] != (0, 0, 0):
            # Black piece in board1, but not in board2, not equal
            return False
        if board1[i] == (255, 250, 250) and board2[i] != (255, 250, 250):
            # White piece in board1, but not in board2, not equal
            return False
    
    # If all positions are equal, return True
    return True


if __name__ == '__main__':
   # Initialize the pygame library
    pygame.init()
    # Initialize the font module of pygame
    pygame.font.init()

    # Define hardness levels mapping
    hardness = {0: EASY, 1: NORMAL, 2: HARD}

    # Enter an infinite loop for the game
    while True:
        # Set frames per second
        FPS = 29
        # Set up the game window with dimensions (WIDTH // 2, HEIGHT)
        WIN = pygame.display.set_mode((WIDTH // 2, HEIGHT))
        # Set the window caption to 'Checkers'
        pygame.display.set_caption('Checkers')
        # Set the game window icon
        icon = pygame.transform.scale(ICON, ICON_SIZE)
        pygame.display.set_icon(icon)

        # Display options and get the selected mode
        mode = display_options()

        # Check the selected mode and start the game accordingly
        if mode == PLAYER_VS_PLAYER:
            # Adjust the game window dimensions for the chosen mode
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            # Start the game in player vs. player mode
            start(mode=PLAYER_VS_PLAYER)

        elif mode == PLAYER_VS_AI:
            # Get the AI level for the white player
            levelw = hardness.get(level_options('AI'))
            # Adjust the game window dimensions for the chosen mode
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            # Start the game in player vs. AI mode with the specified AI level for the white player
            start(mode=PLAYER_VS_AI, levelW=levelw)

        elif mode == AI_VS_AI:
            # Get the AI levels for both white and black players
            levelw = hardness.get(level_options('White'))
            levelb = hardness.get(level_options('Black'))
            # Adjust the game window dimensions for the chosen mode
            WIN = pygame.display.set_mode((WIDTH, HEIGHT + 30))
            # Start the game in AI vs. AI mode with the specified AI levels for both players
            start(mode=AI_VS_AI, levelW=levelw, levelB=levelb)
