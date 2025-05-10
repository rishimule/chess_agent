from typing import List, Tuple, TYPE_CHECKING
from .base import Piece, Color

if TYPE_CHECKING:
    from ..board import Board

class Bishop(Piece):
    """A class representing a bishop in chess.
    
    The bishop moves diagonally any number of squares. It cannot jump over other pieces.
    Each player starts with two bishops, one on a light square and one on a dark square.
    
    Attributes:
        color: The color of the bishop (WHITE or BLACK)
        has_moved: Whether the bishop has moved from its initial position
    """
    
    def get_symbol(self) -> str:
        """Get the Unicode symbol for the bishop.
        
        Returns:
            A string containing the Unicode symbol representing the bishop.
            - '♗' for white bishop
            - '♝' for black bishop
        """
        return '♗' if self.color == Color.WHITE else '♝'

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the bishop.
        
        Returns:
            A string containing the ASCII symbol representing the bishop.
            - 'B' for white bishop
            - 'b' for black bishop
        """
        return 'B' if self.color == Color.WHITE else 'b'

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for the bishop from the given position.
        
        The bishop can move diagonally in any direction until it:
        1. Reaches the edge of the board
        2. Encounters another piece (can capture enemy pieces)
        3. Would move through another piece (cannot jump over pieces)
        
        Args:
            start_pos: The current position of the bishop (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square. The list is empty if:
            - The start position is invalid
            - The start position is outside the board
            - The start position contains invalid coordinates
            
        Note:
            This method only checks if the moves are valid according to the bishop's
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
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # NW, NE, SW, SE

        for drow, dcol in directions:
            current_row, current_col = row, col
            while True:
                current_row += drow
                current_col += dcol
                
                # Check if we're still on the board
                if not (0 <= current_row < 8 and 0 <= current_col < 8):
                    break
                
                target = board.get_piece((current_row, current_col))
                if target is None:
                    moves.append((current_row, current_col))
                elif target.color != self.color:
                    moves.append((current_row, current_col))
                    break
                else:  # Same color piece
                    break

        return moves 