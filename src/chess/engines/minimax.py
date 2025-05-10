from typing import Tuple, Optional, List
import random
from ..board import Board
from ..pieces import Color
from ..pieces.pawn import Pawn
from ..pieces.knight import Knight
from ..pieces.bishop import Bishop
from ..pieces.rook import Rook
from ..pieces.queen import Queen
from ..pieces.king import King
from .base import ChessEngine

class MinimaxEngine(ChessEngine):
    """A chess engine that uses the minimax algorithm with alpha-beta pruning.
    
    This engine implements a minimax search with alpha-beta pruning to find the best move.
    It uses piece-square tables and material evaluation for position scoring.
    """
    
    def __init__(self, depth: int = 3):
        """Initialize the minimax engine with specified search depth.
        
        Args:
            depth: The maximum depth to search in the game tree (default: 3)
        """
        super().__init__()
        self.depth = depth
        self.piece_values = {
            Pawn: 100,
            Knight: 320,
            Bishop: 330,
            Rook: 500,
            Queen: 900,
            King: 20000
        }
        
        # Position tables for piece-square evaluation
        self.pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

    def evaluate_position(self, board: Board) -> float:
        """Evaluate the current board position using material and positional factors.
        
        Args:
            board: The current chess board state
            
        Returns:
            A float representing the evaluation score from the perspective of the current player.
            Positive values indicate an advantage for the current player,
            negative values indicate a disadvantage.
            
        Note:
            The evaluation considers:
            - Material value of pieces
            - Pawn structure and positioning
            - Checkmate and stalemate conditions
        """
        if board.is_checkmate(board.current_turn):
            return float(-10000 if board.current_turn == Color.WHITE else 10000)
        
        if board.is_stalemate():
            return 0.0

        score = 0
        # Material evaluation
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece is not None:
                    # Find the piece type using isinstance
                    for piece_type, value in self.piece_values.items():
                        if isinstance(piece, piece_type):
                            if piece.color == Color.WHITE:
                                score += value
                            else:
                                score -= value
                            break

                    # Position evaluation (simplified)
                    if isinstance(piece, Pawn):
                        if piece.color == Color.WHITE:
                            score += self.pawn_table[row * 8 + col]
                        else:
                            score -= self.pawn_table[(7 - row) * 8 + col]

        return float(score) if board.current_turn == Color.WHITE else float(-score)

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """Implement the minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The current chess board state
            depth: The remaining search depth
            alpha: The alpha value for alpha-beta pruning
            beta: The beta value for alpha-beta pruning
            maximizing: Whether the current player is maximizing (True) or minimizing (False)
            
        Returns:
            A tuple containing:
            - The evaluation score for the position
            - The best move found (start_pos, end_pos) or None if no moves available
        """
        if depth == 0 or board.is_checkmate(board.current_turn) or board.is_stalemate():
            return self.evaluate_position(board), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in self._get_all_moves(board):
                start_pos, end_pos = move
                # Try the move
                if board.make_move(start_pos, end_pos):
                    eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                    board.undo_move()
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self._get_all_moves(board):
                start_pos, end_pos = move
                # Try the move
                if board.make_move(start_pos, end_pos):
                    eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                    board.undo_move()
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def _get_all_moves(self, board: Board) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for the current player.
        
        Args:
            board: The current chess board state
            
        Returns:
            A list of tuples, where each tuple contains:
            - The starting position (row, col)
            - The ending position (row, col)
            
        Note:
            Only returns moves that are legal according to chess rules
            and don't leave the king in check.
        """
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == board.current_turn:
                    for end_pos in piece.get_valid_moves((row, col), board):
                        # Only add moves that don't leave the king in check
                        if board.is_valid_move((row, col), end_pos):
                            moves.append(((row, col), end_pos))
        return moves

    def get_best_move(self, board: Board) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get the best move for the current position using minimax search.
        
        Args:
            board: The current chess board state
            
        Returns:
            A tuple of (start_position, end_position) representing the best move,
            where each position is a tuple of (row, col) coordinates.
            Returns None if no valid moves are available.
            
        Note:
            If no best move is found through minimax search (which shouldn't happen),
            returns a random legal move as a fallback.
        """
        _, best_move = self.minimax(board, self.depth, float('-inf'), float('inf'), board.current_turn == Color.WHITE)
        if best_move is None:
            # If no best move is found (shouldn't happen), return a random legal move
            moves = self._get_all_moves(board)
            return random.choice(moves) if moves else None
        return best_move 