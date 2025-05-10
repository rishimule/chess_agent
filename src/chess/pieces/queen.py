from typing import List, Tuple, TYPE_CHECKING
from .base import Piece, Color

if TYPE_CHECKING:
    from ..board import Board

class Queen(Piece):
    """A class representing a queen in chess.
    
    The queen is the most powerful piece in chess, combining the movement capabilities
    of both the rook and bishop. It can move any number of squares in any direction:
    horizontally, vertically, or diagonally. Each player starts with one queen.
    
    Attributes:
        color: The color of the queen (WHITE or BLACK)
        has_moved: Whether the queen has moved from its initial position
    """
    
    def get_symbol(self) -> str:
        """Get the Unicode symbol for the queen.
        
        Returns:
            A string containing the Unicode symbol representing the queen.
            - '♕' for white queen
            - '♛' for black queen
        """
        return '♕' if self.color == Color.WHITE else '♛'

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the queen.
        
        Returns:
            A string containing the ASCII symbol representing the queen.
            - 'Q' for white queen
            - 'q' for black queen
        """
        return 'Q' if self.color == Color.WHITE else 'q'

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for the queen from the given position.
        
        The queen can move in any direction (horizontally, vertically, or diagonally)
        any number of squares until it:
        1. Reaches the edge of the board
        2. Encounters another piece (can capture enemy pieces)
        3. Would move through another piece (cannot jump over pieces)
        
        Args:
            start_pos: The current position of the queen (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square. The list is empty if:
            - The start position is invalid
            - The start position is outside the board
            - The start position contains invalid coordinates
            
        Note:
            This method only checks if the moves are valid according to the queen's
            movement rules. It does not check if the moves would leave the king in check.
            That check is performed by the Board class.
        """
        # Input validation
        try:
            row, col = start_pos
            if not (isinstance(row, int) and isinstance(col, int)):
                return []
            if not (0 <= row < 8 and 0 <= col < 8):
                return []
        except (TypeError, ValueError):
            return []

        moves = []
        # Queen combines rook and bishop movements
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for drow, dcol in directions:
            current_row, current_col = row + drow, col + dcol
            while 0 <= current_row < 8 and 0 <= current_col < 8:
                target = board.get_piece((current_row, current_col))
                if target is None:
                    moves.append((current_row, current_col))
                elif target.color != self.color:
                    moves.append((current_row, current_col))
                    break
                else:
                    break
                current_row += drow
                current_col += dcol

        return moves 