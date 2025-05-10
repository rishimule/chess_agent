from typing import List, Tuple, Optional, TYPE_CHECKING
from .base import Piece, Color

if TYPE_CHECKING:
    from ..board import Board

class Pawn(Piece):
    """A class representing a pawn in chess.
    
    The pawn is the most numerous piece in chess. Each player starts with eight pawns.
    Pawns have unique movement rules:
    - Move forward one square (cannot move backward)
    - On their first move, can move forward two squares
    - Capture diagonally one square forward
    - Can perform en passant capture under specific conditions
    - Can be promoted to any other piece (except king) upon reaching the opposite end
    
    Attributes:
        color: The color of the pawn (WHITE or BLACK)
        has_moved: Whether the pawn has moved from its initial position
    """
    
    def get_symbol(self) -> str:
        """Get the Unicode symbol for the pawn.
        
        Returns:
            A string containing the Unicode symbol representing the pawn.
            - '♙' for white pawn
            - '♟' for black pawn
        """
        return '♙' if self.color == Color.WHITE else '♟'

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the pawn.
        
        Returns:
            A string containing the ASCII symbol representing the pawn.
            - 'P' for white pawn
            - 'p' for black pawn
        """
        return 'P' if self.color == Color.WHITE else 'p'

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for the pawn from the given position.
        
        The pawn can move in the following ways:
        1. Forward moves:
           - One square forward (if the square is empty)
           - Two squares forward from starting position (if both squares are empty)
        2. Captures:
           - Diagonal capture of enemy pieces
           - En passant capture of enemy pawns that just moved two squares
        
        Args:
            start_pos: The current position of the pawn (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square. The list is empty if:
            - The start position is invalid
            - The start position is outside the board
            - The start position contains invalid coordinates
            
        Note:
            This method only checks if the moves are valid according to the pawn's
            movement rules. It does not check if the moves would leave the king in check.
            That check is performed by the Board class.
            
            Promotion is handled by the Board class when the pawn reaches the opposite end.
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
        direction = -1 if self.color == Color.WHITE else 1

        # Forward move
        if 0 <= row + direction < 8 and board.get_piece((row + direction, col)) is None:
            moves.append((row + direction, col))
            # Double move from starting position
            if not self.has_moved and board.get_piece((row + 2 * direction, col)) is None:
                moves.append((row + 2 * direction, col))

        # Captures
        for dcol in [-1, 1]:
            capture_col = col + dcol
            if 0 <= capture_col < 8:
                # Regular capture
                capture_pos = (row + direction, capture_col)
                if 0 <= capture_pos[0] < 8:  # Make sure capture position is on board
                    target = board.get_piece(capture_pos)
                    if target and target.color != self.color:
                        moves.append(capture_pos)
                    
                    # En passant capture
                    if board.en_passant_target == capture_pos:
                        moves.append(capture_pos)

        return moves 