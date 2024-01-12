import copy
from copy import deepcopy
from .constants import WHITE, BLACK, ROWS
import pygame


def max_value(position, depth, game):
    action = None
    new_value = 0
    if depth == 0 or position.winner() is not None:
        return position, position.evaluate()
    states = get_all_moves(position, BLACK, game)
    depth -= 1
    v = float('-inf')
    for state in states:
        _, new_value = min_value(state, depth, game)
        print(new_value, 'MAX')
        if max(v, new_value) > v:
            v = new_value
            action = state
    return action, v


def min_value(position, depth, game):
    action = None
    new_value = 0
    if depth == 0 or position.winner() is not None:
        return position, position.evaluate()
    depth -= 1
    states = get_all_moves(position, WHITE, game)
    v = float('inf')
    for state in states:
        _, new_value = max_value(state, depth, game)
        print(new_value, 'MIN')
        if min(v, new_value) < v:
            v = new_value
            action = state
    return action, v


def minimax(position, depth, max_player, game):
    if max_player:
        action, v = max_value(position, depth, game)
    else:
        action, v = min_value(position, depth, game)
    return v, action


def minimax_alpha_beta(position, depth, max_player, game, stuck_board):
    if max_player:
        action, v = max_value_alpha_beta(position, depth, game, float('-inf'), float('inf'), stuck_board)
    else:
        action, v = min_value_alpha_beta(position, depth, game, float('-inf'), float('inf'), stuck_board)
    return v, action


def max_value_alpha_beta(position, depth, game, a, b, stuck_board):
    action = None
    new_value = 0
    if depth == 0 or position.winner() is not None:
        return position, position.evaluate()
    states = get_all_moves(position, BLACK, game, stuck_board)
    depth -= 1
    v = float('-inf')
    for state in states:
        _, new_value = min_value_alpha_beta(state, depth, game, a, b, stuck_board)
        if max(v, new_value) > v:
            v = new_value
            action = state
        if v > b:
            return action, v
        a = max(a, v)
    return action, v


def min_value_alpha_beta(position, depth, game, a, b, stuck_board):
    action = None
    new_value = 0
    if depth == 0 or position.winner() is not None:
        return position, position.evaluate()
    depth -= 1
    states = get_all_moves(position, WHITE, game, stuck_board)
    v = float('inf')
    for state in states:
        _, new_value = max_value_alpha_beta(state, depth, game, a, b, stuck_board)
        if min(v, new_value) < v:
            v = new_value
            action = state
        if v <= a:
            return action, v
        b = min(b, v)

    return action, v


def minimax_with_forward_pruning_beam_search(position, depth, alpha, beta, max_player, game, beam_width=20):
    if position is not None:
        if position.winner() == BLACK:
            print("Black is winner")
            return float('-inf'), None

        if position.winner() == WHITE:
            print("White is winner")
            return float('inf'), None

        if depth == 0 or position.winner() is not None:
            return position.evaluate(), None

    else:
        print("Draw")
        return 0, None

    if max_player:
        maxEval = float('-inf')
        best_moves = []

        moves = get_all_moves(position, WHITE, game)
        # Use beam search to keep only top moves based on beam width
        moves = sorted(moves, key=lambda move:
        minimax_with_forward_pruning_beam_search(move, depth - 1, alpha, beta, False, game, beam_width)[0],
                       reverse=True)[:beam_width]

        for move in moves:
            evaluation = \
                minimax_with_forward_pruning_beam_search(move, depth - 1, alpha, beta, False, game, beam_width)[0]
            maxEval = max(maxEval, evaluation)

            if maxEval == evaluation:
                best_moves.append(move)

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                return maxEval, None  # Beta cut-off

        return maxEval, best_moves

    else:
        minEval = float('inf')
        best_moves = []

        moves = get_all_moves(position, BLACK, game)
        # Use beam search to keep only top moves based on beam width
        moves = sorted(moves, key=lambda move:
        minimax_with_forward_pruning_beam_search(move, depth - 1, alpha, beta, True, game, beam_width)[0])[:beam_width]

        for move in moves:
            evaluation = minimax_with_forward_pruning_beam_search(move, depth - 1, alpha, beta, True, game, beam_width)[
                0]
            minEval = min(minEval, evaluation)

            if minEval == evaluation:
                best_moves.append(move)

            beta = min(beta, evaluation)
            if beta <= alpha:
                return minEval, None  # Alpha cut-off

        return minEval, best_moves


def simulate_move(piece, move, board, game, skip):
    temp_board = copy.deepcopy(board)
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game, stuck_board=None):
    pygame.event.pump()
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            if stuck_board is not None and new_board is not None:
                if not compare(new_board.get_board_list(), stuck_board.get_board_list()):
                    moves.append(new_board)
            else:
                moves.append(new_board)

    return moves


def compare(board1, board2):
    for i in range(len(board1)):
        if board1[i] == 0 and board2[i] != 0:
            return False
        if board1[i] == (0, 0, 0) and board2[i] != (0, 0, 0):
            return False
        if board1[i] == (255, 250, 250) and board2[i] != (255, 250, 250):
            return False
    return True
