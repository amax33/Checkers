import copy
import copyreg

import numpy as np
import pygame
from copy import deepcopy
from .constants import *
from .piece import Piece


class Board:
    def __init__(self):
        self.board = [[]]
        self.BLACK_left = self.white_left = 0
        self.BLACK_kings = self.white_kings = 0
        self.create_board()

    def get_board_list(self):
        board = []
        for row in self.board:
            for e in row:
                board.append(e)
        return board

    def draw_cells(self, win):
        win.fill(BEIGE)
        footer = pygame.Rect(0, HEIGHT, WIDTH, 30)
        pygame.draw.rect(win, BLACK, footer)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, BROWN, (row * SQUARE_SIZE,
                                              col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.BLACK_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
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
        self.draw_cells(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            if piece.king:
                if piece.color == WHITE:
                    self.white_kings -= 1
                else:
                    self.BLACK_kings -= 1
            self.board[piece.row][piece.col] = 0

    def winner(self):
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
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        if piece.king and flag:
            new_moves = copy.deepcopy(moves) # Create a copy of moves
            for (r, c) in moves:
                if moves[(r, c)]:
                    temp_board = copy.deepcopy(self)
                    temp_board.board = copy.deepcopy(self.board)
                    temp_board.BLACK_left = np.inf
                    temp_board.white_left = np.inf
                    skip = moves[(r, c)]
                    if skip:
                        temp_board.remove(skip)
                    row = r
                    left = c - 1
                    right = c + 1
                    new_moves.update(temp_board._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left, skipped=moves[(r, c)]))
                    new_moves.update(temp_board._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right, skipped=moves[(r, c)]))
                    new_moves.update(temp_board._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left, skipped=moves[(r, c)]))
                    new_moves.update(temp_board._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right, skipped=moves[(r, c)]))
                moves = self.combine_dict(moves, new_moves)
        return moves

    def combine_dict(self, dict1, dict2):
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
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            # empty square found
            if current == 0:
                # we we skipped over something which is not last and we found a blank square --> break
                if skipped and not last:
                    break
                elif skipped:
                    # double jump
                    moves[(r, left)] = last + skipped
                # if it is zero and last existed that means we can jump over it now
                else:
                    # first one
                    moves[(r, left)] = last

                # here if there was something that we skipped, in this part we prepare for double or tripple jump now
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # now we recalculate where we are going to stop
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            # the piece we are trying to move is same as that of ours so we are blocked hence break
            elif current.color == color:
                break
            # Now we can move over that peice assuming that there is an empty square after that
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            # empty square found
            if current == 0:
                # we skipped over something which is not last and we found a blank square --> break
                if skipped and not last:
                    break
                elif skipped:
                    # double jump
                    moves[(r, right)] = last + skipped
                # if it is zero and last existed that means we can jump over it now
                else:
                    # first one
                    moves[(r, right)] = last

                # here if there was something that we skipped, in this part we prepare for double or tripple jump now
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # now we recalculate where we are going to stop
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            # the piece we are trying to move is same as that of ours so we are blocked hence break
            elif current.color == color:
                break
            # Now we can move over that piece assuming that there is an empty square after that
            else:
                last = [current]
            right += 1
        return moves

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def evaluate(self):
        white_score = 0
        black_score = 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    # Feature 1: Material Count
                    if piece.color == WHITE:
                        white_score += 1
                        if piece.king:
                            white_score += 1
                    elif piece.color == BLACK:
                        black_score += 1
                        if piece.king:
                            black_score += 1

                    # Feature 3: Piece Advancement
                    if piece.color == WHITE and not piece.king:
                        if piece.row == ROWS - 1:
                            white_score += 2
                            black_score -= 1
                    elif piece.color == BLACK and not piece.king:
                        if piece.row == 0:
                            black_score += 2
                            white_score -= 1
                    # Feature 4: Control of the Center
                    center_row = ROWS // 2
                    if piece.row == center_row:
                        white_score += 1 if piece.color == WHITE else 0
                        black_score += 1 if piece.color == BLACK else 0

                    # Feature 5: King Safety (evaluate based on proximity to opponent pieces)
                    if piece.color == WHITE and piece.king and self.BLACK_kings > self.white_kings:
                        # Penalize positions where white kings are vulnerable
                        for opp_piece in self.get_all_pieces(BLACK):
                            if opp_piece.row == piece.row + 1 and abs(opp_piece.col - piece.col) == 1:
                                white_score -= 1
                                black_score += 1
                                break
                    elif piece.color == BLACK and piece.king and self.white_kings > self.BLACK_kings:
                        # Penalize positions where black kings are vulnerable
                        for opp_piece in self.get_all_pieces(WHITE):
                            if opp_piece.row == piece.row + 1 and abs(opp_piece.col - piece.col) == 1:
                                black_score -= 1
                                white_score += 1
                                break

                    # Feature 6: Encourage double/triple jumps
                    moves_count = self.get_valid_moves(piece)
                    for move in moves_count:
                        if len(move) >= 2:
                            if piece.color == WHITE:
                                white_score += 1
                                black_score -= 1
                            elif piece.color == BLACK:
                                black_score += 1
                                white_score -= 1

        return black_score - white_score
