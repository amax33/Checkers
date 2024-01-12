import copy
import copyreg
import numpy as np
import pygame
from copy import deepcopy
from .constants import *
from .piece import Piece

# Board class definition


class Board:
    def __init__(self):
        # Initialize board properties
        self.board = [[]]
        self.BLACK_left = self.white_left = 0
        self.BLACK_kings = self.white_kings = 0
        self.create_board()

    def get_board_list(self):
        # Flatten the board into a list for comparison purposes
        board = []
        for row in self.board:
            for e in row:
                board.append(e)
        return board

    def draw_cells(self, win):
        # Draw the game board cells and background
        win.fill(BEIGE)
        footer = pygame.Rect(0, HEIGHT, WIDTH, 30)
        pygame.draw.rect(win, BLACK, footer)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, BROWN, (row * SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        # Move a piece to a new position on the board
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.BLACK_kings += 1

    def get_piece(self, row, col):
        # Get the piece at a specific position on the board
        return self.board[row][col]

    def create_board(self):
        # Create the initial game board
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append((Piece(row, col, WHITE)))
                    elif row > 4:
                        self.board[row].append((Piece(row, col, BLACK)))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        # Draw the entire game board
        self.draw_cells(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        # Remove pieces from the board
        for piece in pieces:
            if piece.king:
                if piece.color == WHITE:
                    self.white_kings -= 1
                else:
                    self.BLACK_kings -= 1
            self.board[piece.row][piece.col] = 0

    def winner(self):
        # Determine the winner of the game
        black_move = 0
        white_move = 0
        for row in self.board:
            for e in row:
                if isinstance(e, Piece):
                    if e.color == BLACK:
                        self.BLACK_left += 1
                        if black_move <= 0:
                            black_move += len(self.get_valid_moves(e))
                    elif e.color == WHITE:
                        if white_move <= 0:
                            white_move += len(self.get_valid_moves(e))
                        self.white_left += 1
        if self.BLACK_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        else:
            self.BLACK_left = 0
            self.white_left = 0
        if black_move == 0 and white_move == 0:
            return GRAY
        if black_move == 0:
            return WHITE
        if white_move == 0:
            return BLACK
        return None

    def get_valid_moves(self, piece, flag=True):
        # Get valid moves for a given piece
        # Initialize an empty dictionary to store possible moves for the given piece
        moves = {}

        # Set initial values for left, right, and row based on the piece's current position
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Check if the piece is either a BLACK piece or a king
        if piece.color == BLACK or piece.king:
            # Update moves using valid moves from traversing left and right for BLACK or king pieces
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        # Check if the piece is either a WHITE piece or a king
        if piece.color == WHITE or piece.king:
            # Update moves using valid moves from traversing left and right for WHITE or king pieces
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        # Check if the piece is a king and the flag is set to True
        if piece.king and flag:
            # Create a deep copy of the current moves
            new_moves = copy.deepcopy(moves)

            # Iterate over the existing moves
            for (r, c) in moves:
                if moves[(r, c)]:
                    # Create a deep copy of the current board state
                    temp_board = copy.deepcopy(self)
                    temp_board.board = copy.deepcopy(self.board)
                    temp_board.BLACK_left = np.inf
                    temp_board.white_left = np.inf

                    # Get the skipped pieces and remove them from the temporary board state
                    skip = moves[(r, c)]
                    if skip:
                        temp_board.remove(skip)

                    # Update row, left, and right values
                    row = r
                    left = c - 1
                    right = c + 1

                    # Update new_moves with valid moves from traversing left and right after a possible jump
                    new_moves.update(temp_board._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left,
                                                            skipped=moves[(r, c)]))
                    new_moves.update(temp_board._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right,
                                                                skipped=moves[(r, c)]))
                    new_moves.update(temp_board._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left,
                                                            skipped=moves[(r, c)]))
                    new_moves.update(temp_board._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right,
                                                                skipped=moves[(r, c)]))

            # Combine the original moves with the new_moves, considering multiple jumps
            moves = self.combine_dict(moves, new_moves)
        return moves

    def combine_dict(self, dict1, dict2):
        # Combine two dictionaries
        combined_dict = {}
        # Merge dictionaries
        for key, value in dict1.items():
            if key in dict2:
                combined_dict[key] = value + dict2[key]
            else:
                combined_dict[key] = value

        # Add remaining keys from dict2
        for key, value in dict2.items():
            if key not in combined_dict:
                combined_dict[key] = value
        return combined_dict

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        # Helper function
        # Traverse left to find valid moves for a piece
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            # Empty square found
            if current == 0:
                # We skipped over something which is not last and found a blank square, break
                if skipped and not last:
                    break
                elif skipped:
                    # Double jump
                    moves[(r, left)] = last + skipped
                # If it is zero and last existed, we can jump over it now
                else:
                    # First one
                    moves[(r, left)] = last

                # If there was something skipped, prepare for double or triple jump
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # Recalculate where we are going to stop
                    moves.update(self._traverse_left(
                        r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(
                        r + step, row, step, color, left + 1, skipped=last))
                break
            # The piece we are trying to move is the same color as ours, so we are blocked, break
            elif current.color == color:
                break
            # Now we can move over that piece assuming there is an empty square after that
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        # Helper function to traverse right and find valid moves for a piece
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            # Empty square found
            if current == 0:
                # We skipped over something which is not last and found a blank square, break
                if skipped and not last:
                    break
                elif skipped:
                    # Double jump
                    moves[(r, right)] = last + skipped
                # If it is zero and last existed, we can jump over it now
                else:
                    # First one
                    moves[(r, right)] = last

                # If there was something skipped, prepare for double or triple jump
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # Recalculate where we are going to stop
                    moves.update(self._traverse_left(
                        r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(
                        r + step, row, step, color, right + 1, skipped=last))
                break
            # The piece we are trying to move is the same color as ours, so we are blocked, break
            elif current.color == color:
                break
            # Now we can move over that piece assuming there is an empty square after that
            else:
                last = [current]
            right += 1
        return moves

    def get_all_pieces(self, color):
        # Get all pieces of a specified color
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def evaluate(self):
        # Evaluate the current board state based on various features
        white_score = 0
        black_score = 0

        # Iterate through each row and piece on the board
        for row in self.board:
            for piece in row:
                # Check if the current position is not empty
                if piece != 0:
                    # Feature 1: Material Count
                    if piece.color == WHITE:
                        white_score += 1
                        # Bonus score for kings
                        if piece.king:
                            white_score += 1
                    elif piece.color == BLACK:
                        black_score += 1
                        # Bonus score for kings
                        if piece.king:
                            black_score += 1

                    # Feature 3: Piece Advancement
                    if piece.color == WHITE and not piece.king:
                        # Bonus score for non-king white pieces reaching the opposite end
                        if piece.row == ROWS - 1:
                            white_score += 2
                            black_score -= 1
                    elif piece.color == BLACK and not piece.king:
                        # Bonus score for non-king black pieces reaching the opposite end
                        if piece.row == 0:
                            black_score += 2
                            white_score -= 1

                    # Feature 4: Control of the Center
                    center_row = ROWS // 2
                    if piece.row == center_row:
                        # Bonus score for pieces in the center row
                        white_score += 1 if piece.color == WHITE else 0
                        black_score += 1 if piece.color == BLACK else 0

                    # Feature 5: King Safety (evaluate based on proximity to opponent pieces)
                    if piece.color == WHITE and piece.king and self.BLACK_kings > self.white_kings:
                        # Penalize positions where white kings are vulnerable to capture by black pieces
                        for opp_piece in self.get_all_pieces(BLACK):
                            if opp_piece.row == piece.row + 1 and abs(opp_piece.col - piece.col) == 1:
                                white_score -= 1
                                black_score += 1
                                break
                    elif piece.color == BLACK and piece.king and self.white_kings > self.BLACK_kings:
                        # Penalize positions where black kings are vulnerable to capture by white pieces
                        for opp_piece in self.get_all_pieces(WHITE):
                            if opp_piece.row == piece.row + 1 and abs(opp_piece.col - piece.col) == 1:
                                black_score -= 1
                                white_score += 1
                                break

                    # Feature 6: Encourage double/triple jumps
                    moves_count = self.get_valid_moves(piece)
                    for move in moves_count:
                        if len(move) >= 2:
                            # Bonus score for pieces capable of double or triple jumps
                            if piece.color == WHITE:
                                white_score += 1
                                black_score -= 1
                            elif piece.color == BLACK:
                                black_score += 1
                                white_score -= 1

        # Return the difference between black_score and white_score as the final evaluation
        return black_score - white_score
