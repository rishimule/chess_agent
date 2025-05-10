from typing import List, Tuple, TYPE_CHECKING
from .base import Piece, Color

if TYPE_CHECKING:
    from ..board import Board

class Rook(Piece):
    """A class representing a rook in chess.
    
    The rook moves horizontally or vertically any number of squares. It cannot jump over
    other pieces. Each player starts with two rooks, one in each corner. The rook is
    involved in the special castling move with the king.
    
    Attributes:
        color: The color of the rook (WHITE or BLACK)
        has_moved: Whether the rook has moved from its initial position
    """
    
    def get_symbol(self) -> str:
        """Get the Unicode symbol for the rook.
        
        Returns:
            A string containing the Unicode symbol representing the rook.
            - '♖' for white rook
            - '♜' for black rook
        """
        return '♖' if self.color == Color.WHITE else '♜'

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the rook.
        
        Returns:
            A string containing the ASCII symbol representing the rook.
            - 'R' for white rook
            - 'r' for black rook
        """
        return 'R' if self.color == Color.WHITE else 'r'

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for the rook from the given position.
        
        The rook can move horizontally or vertically any number of squares until it:
        1. Reaches the edge of the board
        2. Encounters another piece (can capture enemy pieces)
        3. Would move through another piece (cannot jump over pieces)
        
        Args:
            start_pos: The current position of the rook (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square. The list is empty if:
            - The start position is invalid
            - The start position is outside the board
            - The start position contains invalid coordinates
            
        Note:
            This method only checks if the moves are valid according to the rook's
            movement rules. It does not check if the moves would leave the king in check.
            That check is performed by the Board class.
            
            The rook's has_moved attribute is used by the Board class to determine
            if castling is possible with the king.
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
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

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