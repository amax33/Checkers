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


def minimax_alpha_beta(position, depth, max_player, game, stuck_board, prune=False):
    if max_player:
        action, v = max_value_alpha_beta(position, depth, game, float('-inf'), float('inf'), stuck_board, prune)
    else:
        action, v = min_value_alpha_beta(position, depth, game, float('-inf'), float('inf'), stuck_board, prune)
    return v, action


def max_value_alpha_beta(position, depth, game, a, b, stuck_board, prune):
    action = None
    new_value = 0
    if depth == 0 or position.winner() is not None:
        return position, position.evaluate()
    depth -= 1
    if prune:
        states = forward_pruning(position, BLACK, game, stuck_board)
    else:
        states = get_all_moves(position, BLACK, game, stuck_board)
    if len(states) == 0:
        return None, float('inf')
    v = a
    for state in states:
        _, new_value = min_value_alpha_beta(state, depth, game, a, b, stuck_board, prune)
        if new_value > v:
            v = new_value
            action = state
        a = max(a, v)
        if v >= b:
            return action, v
    return action, v


def min_value_alpha_beta(position, depth, game, a, b, stuck_board, prune):
    action = None
    new_value = 0
    if depth == 0 or position.winner() is not None:
        return position, position.evaluate()
    depth -= 1
    if prune:
        states = forward_pruning(position, WHITE, game, stuck_board)
    else:
        states = get_all_moves(position, WHITE, game, stuck_board)
    if len(states) == 0:
        return None, float('-inf')
    v = b
    for state in states:
        _, new_value = max_value_alpha_beta(state, depth, game, a, b, stuck_board, prune)
        if new_value < v:
            v = new_value
            action = state
        b = min(b, v)
        if v <= a:
            return action, v

    return action, v

def forward_pruning(position, color, game, stuck_board, num_moves_to_consider=2):
    """
    Forward pruning to only consider a limited number of moves based on static evaluation.
    """
    all_moves = get_all_moves(position, color, game, stuck_board)
    evaluated_moves = []

    # Evaluate all moves and sort them
    for move in all_moves:
        evaluated_moves.append((move, move.evaluate()))

    # Sort the moves based on evaluation score
    if color == WHITE:
        # White aims for the lowest score (minimizer)
        evaluated_moves.sort(key=lambda x: x[1])
    else:
        # Black aims for the highest score (maximizer)
        evaluated_moves.sort(key=lambda x: x[1], reverse=True)

    # Select the top 'num_moves_to_consider' moves
    pruned_moves = [move for move, score in evaluated_moves[:num_moves_to_consider]]

    return pruned_moves


def simulate_move(piece, move, board, game, skip):
    temp_board = copy.deepcopy(board)
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game, stuck_board):
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
