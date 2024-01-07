import pygame
from .board import Board
from .constants import *


class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.font = pygame.font.Font('assets/BELL.TTF', 20)  # Adjust the size as needed
        self.start_time = pygame.time.get_ticks()
        self.jumping_state = False


    def update(self):
        print(self.win)
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw_time()
        self.draw_turn()
        pygame.display.update()

    def _init(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected_piece:
            result = self._move(row, col)
            if not result:
                self.selected_piece = None
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected_piece and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE //2), SQUARE_SIZE//3)

    def winner(self):
        return self.board.winner()


    def change_turn(self):
        self.valid_moves = []
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def draw_time(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000  # Convert to seconds
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = f"Time: {minutes}:{seconds:02d}"
        time_surface = self.font.render(time_text, True, GOLD)
        self.win.blit(time_surface, (WIDTH//8, HEIGHT + 3))  # Adjust the position as needed

    def draw_turn(self):
        turn_text = f"Turn: {'Black' if self.turn == BLACK else 'White'}"
        turn_surface = self.font.render(turn_text, True, GOLD)
        self.win.blit(turn_surface, (WIDTH//1.5, HEIGHT + 3))  # Adjust the position and width as needed

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
        
