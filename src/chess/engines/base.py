from abc import ABC, abstractmethod
from typing import Tuple, Optional
from ..board import Board

class ChessEngine(ABC):
    """Base abstract class for all chess engines.
    
    This class defines the interface that all chess engines must implement.
    It provides abstract methods for move generation and position evaluation.
    """
    
    def __init__(self):
        """Initialize the chess engine.
        
        This method should be called by all subclasses to ensure proper initialization.
        """
        pass
    
    @abstractmethod
    def get_best_move(self, board: Board) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get the best move for the current position.
        
        Args:
            board: The current chess board state
            
        Returns:
            A tuple of (start_position, end_position) representing the best move,
            where each position is a tuple of (row, col) coordinates.
            Returns None if no valid moves are available.
            
        Note:
            The returned move should be legal according to chess rules and
            should not leave the king in check.
        """
        pass
    
    @abstractmethod
    def evaluate_position(self, board: Board) -> float:
        """Evaluate the current board position.
        
        Args:
            board: The current chess board state
            
        Returns:
            A float representing the evaluation score from the perspective of the current player.
            Positive values indicate an advantage for the current player,
            negative values indicate a disadvantage.
            
        Note:
            The evaluation should consider factors such as material value,
            piece positioning, and tactical opportunities.
        """
        pass 