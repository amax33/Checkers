from copy import deepcopy
from .constants import WHITE, BLACK, ROWS


MAX_PIECES_THRESHOLD = 12  # Adjust this threshold as needed


def evaluate_board(board):
    white_score = 0
    black_score = 0

    for row in range(ROWS):
        for piece in board[row]:
            if piece is not None:
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
                    white_score -= sum(1 for opp_piece in board.get_all_pieces(BLACK) if opp_piece.row == piece.row - 1 and abs(opp_piece.col - piece.col) == 1)
                elif piece.color == BLACK:
                    # Penalize positions where black kings are vulnerable
                    black_score -= sum(1 for opp_piece in board.get_all_pieces(WHITE) if opp_piece.row == piece.row + 1 and abs(opp_piece.col - piece.col) == 1)

                # Feature 6: Mobility
                # Encourage greater mobility by giving higher scores to positions that allow for more legal moves
                moves_count = len(board.get_valid_moves(piece))
                if piece.color == WHITE:
                    white_score += moves_count
                elif piece.color == BLACK:
                    black_score += moves_count

                # Feature 7: Double and Triple Jumps (not explicitly implemented, but moves_count can indirectly account for this)
                
    return white_score - black_score




def minimax(position, depth, max_player, game):
    if position is not None:
        if position.winner() == BLACK:
            print('Black is winner')
            return ['False', 'False']
        
        if position.winner() == WHITE:
            print('White is winner')
            return ['False', 'False']
        

        if depth == 0 or position.winner() != None:
            return position.evaluate(), position
    else:
        print('Draw')
        return ['False', 'False']
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    
    else:
        minEval = float('inf')
        best_move = None
    
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
    
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move



def minimax_with_alpha_beta(position, depth, alpha, beta, max_player, game):
    if position is not None:
        if position.winner() == BLACK:
            print('Black is winner')
            return ['False', 'False']
        
        if position.winner() == WHITE:
            print('White is winner')
            return ['False', 'False']
        
        if depth == 0 or position.winner() is not None:
            return position.evaluate(), None
    else:
        print('Draw')
        return ['False', 'False']
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax_with_alpha_beta(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)
            
            if maxEval == evaluation:
                best_move = move
            
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Beta cut-off
                
        return maxEval, best_move
    
    else:
        minEval = float('inf')
        best_move = None
    
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax_with_alpha_beta(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
    
            if minEval == evaluation:
                best_move = move
            
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Alpha cut-off
        
        return minEval, best_move




def minimax_with_forward_pruning(position, depth, alpha, beta, max_player, game):
    if position is not None:
        if position.winner() == BLACK:
            print("Black is winner")
            return float('-inf'), None

        if position.winner() == WHITE:
            print("White is winner")
            return float('inf'), None

        if depth == 0 or position.winner() is not None:
            return 0, None

    else:
        return 0, None

    # Forward pruning based on the number of pieces
    if len(position.get_all_pieces(WHITE)) + len(position.get_all_pieces(BLACK)) > MAX_PIECES_THRESHOLD:
        return 0, None

    if max_player:
        maxEval = float('-inf')
        best_move = None

        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax_with_forward_pruning(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)

            if maxEval == evaluation:
                best_move = move

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                return maxEval, None  # Beta cut-off

        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None

        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax_with_forward_pruning(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)

            if minEval == evaluation:
                best_move = move

            beta = min(beta, evaluation)
            if beta <= alpha:
                return minEval, None  # Alpha cut-off

        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


