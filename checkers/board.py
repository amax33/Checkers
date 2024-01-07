import pygame
from .constants import *
from .piece import Piece


class Board:
    def __init__(self):
        self.board = [[]]
        self.BLACK_left = self.white_left = 12
        self.BLACK_kings = self.white_kings = 0
        self.create_board()

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
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.BLACK_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.BLACK_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK

    def get_valid_moves(self, piece):
        moves = {}  # (4,5): [(3,4)]
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK and not piece.king:
            moves.update(self._traverse_left(
                row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(
                row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE and not piece.king:
            moves.update(self._traverse_left(
                row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(
                row + 1, min(row + 3, ROWS), 1, piece.color, right))

        if piece.king:
            # Store the current state of the moves dictionary
            previous_moves = dict(moves)

            moves.update(self._traverse_left(
                row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_left(
                row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(
                row - 1, max(row - 3, -1), -1, piece.color, right))
            moves.update(self._traverse_right(
                row + 1, min(row + 3, ROWS), 1, piece.color, right))

            # Check if the moves dictionary has changed

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        :start: The starting row index for traversal.
        :stop: The stopping row index for traversal.
        :step: The direction of traversal (1 for moving down, -1 for moving up).
        :color: The color of the current piece.
        :left: The initial column index for traversal.
        :skipped: A list to keep track of any opponent pieces that have been skipped.
        """

        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(
                        r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(
                        r + step, row, step, color, left + 1, skipped=last))
                break

            elif current.color == color:
                break
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
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(
                        r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(
                        r + step, row, step, color, right + 1, skipped=last))
                break

            elif current.color == color:
                break
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

    def _get_jump_moves(self, piece, direction, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(piece.row + direction, piece.row + direction * 3, step):
            if col < 0 or col >= COLS:
                break
            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = last + skipped
                else:
                    moves[(r, col)] = last

                if last:
                    next_col = col - 1 if step == -1 else col + 1
                    moves.update(self._get_jump_moves(
                        piece, direction, step, color, next_col, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            col += 1
        return moves
    

    def _count_jumps(self, piece):
        jump_count = 0

        if piece.color == BLACK and not piece.king:
            jump_count += self._count_jump_moves(
                piece, -1, piece.row - 2, -1, piece.color, piece.col - 2)
            jump_count += self._count_jump_moves(
                piece, -1, piece.row - 2, 1, piece.color, piece.col + 2)

        if piece.color == WHITE and not piece.king:
            jump_count += self._count_jump_moves(
                piece, 1, piece.row + 2, -1, piece.color, piece.col - 2)
            jump_count += self._count_jump_moves(
                piece, 1, piece.row + 2, 1, piece.color, piece.col + 2)

        if piece.king:
            jump_count += self._count_jump_moves(
                piece, -1, piece.row - 2, -1, piece.color, piece.col - 2)
            jump_count += self._count_jump_moves(
                piece, -1, piece.row - 2, 1, piece.color, piece.col + 2)
            jump_count += self._count_jump_moves(
                piece, 1, piece.row + 2, -1, piece.color, piece.col - 2)
            jump_count += self._count_jump_moves(
                piece, 1, piece.row + 2, 1, piece.color, piece.col + 2)

        return jump_count

    def _count_jump_moves(self, piece, direction, stop, step, color, col):
        jump_count = 0
        for r in range(piece.row + direction, stop, step):
            if 0 <= r < ROWS and 0 <= col < COLS:  # Check if indices are within valid range
                current = self.board[r][col]
                if current == 0:
                    break
                elif current.color == color:
                    break
                else:
                    next_col = col + 1 if step == -1 else col - 1
                    if 0 <= r + direction < ROWS and 0 <= next_col < COLS:  # Check if indices are within valid range
                        next_square = self.board[r + direction][next_col]
                        if next_square == 0:
                            jump_count += 1
                        col += 2
                    else:
                        break
            else:
                break

        return jump_count


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

                    # Feature 2: King Proximity
                    if piece.king:
                        # Encourage kings to be positioned in the center of the board
                        white_score += 1 if piece.color == WHITE else 0
                        black_score += 1 if piece.color == BLACK else 0

                    # Feature 3: Piece Advancement
                    if piece.color == WHITE:
                        white_score += piece.row
                    elif piece.color == BLACK:
                        black_score += ROWS - 1 - piece.row

                    # Feature 4: Control of the Center
                    center_row = ROWS // 2
                    if piece.row == center_row:
                        white_score += 1 if piece.color == WHITE else 0
                        black_score += 1 if piece.color == BLACK else 0

                    # Feature 5: King Safety (evaluate based on proximity to opponent pieces)
                    if piece.color == WHITE:
                        # Penalize positions where white kings are vulnerable
                        white_score -= sum(1 for opp_piece in self.get_all_pieces(
                            BLACK) if opp_piece.row == piece.row - 1 and abs(opp_piece.col - piece.col) == 1)
                    elif piece.color == BLACK:
                        # Penalize positions where black kings are vulnerable
                        black_score -= sum(1 for opp_piece in self.get_all_pieces(
                            WHITE) if opp_piece.row == piece.row + 1 and abs(opp_piece.col - piece.col) == 1)

                    # Feature 6: Mobility
                    # Encourage greater mobility by giving higher scores to positions that allow for more legal moves
                    moves_count = len(self.get_valid_moves(piece))
                    if piece.color == WHITE:
                        white_score += moves_count
                    elif piece.color == BLACK:
                        black_score += moves_count

                    # New Feature: Jump Count
                    jump_count = self._count_jumps(piece)
                    if piece.color == WHITE:
                        white_score += jump_count
                    elif piece.color == BLACK:
                        black_score += jump_count


        return white_score - black_score
