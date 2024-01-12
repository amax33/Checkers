import pygame
from .board import Board
from .constants import *

class Game:
    def __init__(self, win):
        self._init()  # Initialize internal attributes
        self.win = win
        # Adjust the size as needed
        self.font = pygame.font.Font('assets/BELL.TTF', 20)
        self.start_time = pygame.time.get_ticks()
        self.jumping_state = False  # Flag for jumping state in the game

    # Update method to refresh the game state on the window
    def update(self):
        self.board.draw(self.win)  # Draw the game board
        self.draw_valid_moves(self.valid_moves)  # Draw valid move indicators
        self.draw_selected_piece()  # Draw selection highlight for a piece
        self.draw_time()  # Draw the elapsed time
        self.draw_turn()  # Draw the current turn
        pygame.display.update()  # Update the display

    # Draw a highlight around the selected piece
    def draw_selected_piece(self):
        if self.selected_piece:
            row, col = self.selected_piece.row, self.selected_piece.col
            pygame.draw.rect(self.win, GRAY, (col * SQUARE_SIZE,
                                              row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=5)

    # Initialize the game state
    def _init(self):
        self.selected_piece = None  # Currently selected piece
        self.board = Board()  # Game board
        self.turn = BLACK  # Current turn color
        self.valid_moves = {}  # Valid moves for the selected piece

    def reset(self):
        self._init()

    # Handle player move selection
    def select(self, row, col):
        if self.selected_piece:
            result = self._move(row, col)  # Attempt to move to the selected position
            if not result:
                self.selected_piece = None  # Clear selection if the move is not valid
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    # Execute the selected move
    def _move(self, row, col):
        # Get the piece at the specified row and column
        piece = self.board.get_piece(row, col)

        # Check if there is a selected piece, the target position is empty, and the move is valid
        if self.selected_piece and piece == 0 and (row, col) in self.valid_moves:
            # Move the selected piece to the target position
            self.board.move(self.selected_piece, row, col)
            
            # Check if there is a piece that was skipped during the move and remove it
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            
            # Switch the turn to the other player
            self.change_turn()
        else:
            # Return False if the move is not valid
            return False

        # Return True if the move was successfully executed
        return True

    # Draw indicators for valid moves
    def draw_valid_moves(self, moves):
        for move in moves:
            # Extract the row and column from the current move
            row, col = move
            
            # Define star coordinates for move indicators
            star_points = [
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 8),
                (col * SQUARE_SIZE + SQUARE_SIZE * 3 // 8, row * SQUARE_SIZE + SQUARE_SIZE * 3 // 8),
                (col * SQUARE_SIZE + SQUARE_SIZE // 8, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                (col * SQUARE_SIZE + SQUARE_SIZE * 3 // 8, row * SQUARE_SIZE + SQUARE_SIZE * 5 // 8),
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE - SQUARE_SIZE // 8),
                (col * SQUARE_SIZE + SQUARE_SIZE * 5 // 8, row * SQUARE_SIZE + SQUARE_SIZE * 5 // 8),
                ((col + 1) * SQUARE_SIZE - SQUARE_SIZE // 8, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                (col * SQUARE_SIZE + SQUARE_SIZE * 5 // 8, row * SQUARE_SIZE + SQUARE_SIZE * 3 // 8),
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 8)
            ]
            
            # Draw a polygon (star) on the game window using the defined coordinates and color (GRAY)
            pygame.draw.polygon(self.win, GRAY, star_points)

    def winner(self):
        return self.board.winner()

    def change_turn(self):
        self.valid_moves = []
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    # Draw the elapsed time
    def draw_time(self):
        current_time = pygame.time.get_ticks()
        # Convert to seconds
        elapsed_time = (current_time - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = f"Time: {minutes}:{seconds:02d}"
        time_surface = self.font.render(time_text, True, GOLD)
        self.win.blit(time_surface, (WIDTH // 8, HEIGHT + 3))

    # Draw the current turn information
    def draw_turn(self):
        turn_text = f"Turn: {'Black' if self.turn == BLACK else 'White'}"
        turn_surface = self.font.render(turn_text, True, GOLD)
        # Adjust the position and width as needed
        self.win.blit(turn_surface, (WIDTH // 1.5, HEIGHT + 3))

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
