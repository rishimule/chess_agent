from typing import List, Tuple, TYPE_CHECKING
from .base import Piece, Color

if TYPE_CHECKING:
    from ..board import Board

class Knight(Piece):
    """A class representing a knight in chess.
    
    The knight moves in an L-shape pattern: two squares in one direction (horizontal or vertical)
    and then one square perpendicular to that direction. The knight is the only piece that can
    jump over other pieces. Each player starts with two knights.
    
    Attributes:
        color: The color of the knight (WHITE or BLACK)
        has_moved: Whether the knight has moved from its initial position
    """
    
    def get_symbol(self) -> str:
        """Get the Unicode symbol for the knight.
        
        Returns:
            A string containing the Unicode symbol representing the knight.
            - '♘' for white knight
            - '♞' for black knight
        """
        return '♘' if self.color == Color.WHITE else '♞'

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the knight.
        
        Returns:
            A string containing the ASCII symbol representing the knight.
            - 'N' for white knight
            - 'n' for black knight
        """
        return 'N' if self.color == Color.WHITE else 'n'

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for the knight from the given position.
        
        The knight can move in an L-shape pattern:
        - Two squares horizontally and one square vertically, or
        - Two squares vertically and one square horizontally
        
        The knight can:
        - Jump over other pieces (unlike other pieces)
        - Capture enemy pieces by landing on their square
        - Move to any empty square within its range
        
        Args:
            start_pos: The current position of the knight (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square. The list is empty if:
            - The start position is invalid
            - The start position is outside the board
            - The start position contains invalid coordinates
            
        Note:
            This method only checks if the moves are valid according to the knight's
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
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for drow, dcol in knight_moves:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board.get_piece((new_row, new_col))
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))

        return moves 