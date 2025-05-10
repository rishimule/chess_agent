from typing import List, Tuple, TYPE_CHECKING
from .base import Piece, Color
from .rook import Rook

if TYPE_CHECKING:
    from ..board import Board

class King(Piece):
    """A class representing a king in chess.
    
    The king moves one square in any direction (horizontally, vertically, or diagonally).
    It can also perform a special move called castling with a rook under certain conditions.
    The king is the most important piece in chess - if it is checkmated, the game is lost.
    
    Attributes:
        color: The color of the king (WHITE or BLACK)
        has_moved: Whether the king has moved from its initial position
    """
    
    def get_symbol(self) -> str:
        """Get the Unicode symbol for the king.
        
        Returns:
            A string containing the Unicode symbol representing the king.
            - '♔' for white king
            - '♚' for black king
        """
        return '♔' if self.color == Color.WHITE else '♚'

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the king.
        
        Returns:
            A string containing the ASCII symbol representing the king.
            - 'K' for white king
            - 'k' for black king
        """
        return 'K' if self.color == Color.WHITE else 'k'

    def is_square_attacked(self, pos: Tuple[int, int], board: 'Board') -> bool:
        """Check if a square is under attack by enemy pieces.
        
        This method checks if any enemy piece can legally move to the given square.
        It checks for attacks from:
        - Pawns (diagonal captures)
        - Knights (L-shaped moves)
        - Bishops and Queens (diagonal moves)
        - Rooks and Queens (straight moves)
        - Enemy King (adjacent squares)
        
        Args:
            pos: The position to check (row, col)
            board: The current state of the chess board
            
        Returns:
            True if the square is under attack by any enemy piece, False otherwise.
            
        Note:
            This method is used to check for check and checkmate conditions,
            as well as to validate castling moves.
        """
        row, col = pos
        
        # Check for attacks from pawns
        pawn_directions = [(1, -1), (1, 1)] if self.color == Color.WHITE else [(-1, -1), (-1, 1)]
        for dr, dc in pawn_directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece((r, c))
                if piece and piece.color != self.color and piece.get_ascii_symbol().upper() == 'P':
                    return True

        # Check for attacks from knights
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece((r, c))
                if piece and piece.color != self.color and piece.get_ascii_symbol().upper() == 'N':
                    return True

        # Check for attacks from bishops and queens (diagonal)
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonal_directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece((r, c))
                if piece:
                    if piece.color != self.color and piece.get_ascii_symbol().upper() in ['B', 'Q']:
                        return True
                    break
                r, c = r + dr, c + dc

        # Check for attacks from rooks and queens (straight)
        straight_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in straight_directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece((r, c))
                if piece:
                    if piece.color != self.color and piece.get_ascii_symbol().upper() in ['R', 'Q']:
                        return True
                    break
                r, c = r + dr, c + dc

        # Check for attacks from enemy king
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece((r, c))
                if piece and piece.color != self.color and piece.get_ascii_symbol().upper() == 'K':
                    return True

        return False

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for the king from the given position.
        
        The king can move one square in any direction (horizontally, vertically, or diagonally).
        It can also perform castling if:
        1. Neither the king nor the castling rook has moved
        2. There are no pieces between the king and rook
        3. The king is not in check
        4. The king does not move through or into check
        
        Args:
            start_pos: The current position of the king (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square. The list is empty if:
            - The start position is invalid
            - The start position is outside the board
            - The start position contains invalid coordinates
            
        Note:
            This method only checks if the moves are valid according to the king's
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
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        # Regular moves
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board.get_piece((new_row, new_col))
                # Only add the move if the target square is empty or contains an enemy piece
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))

        # Check if king is currently in check
        if self.is_square_attacked(start_pos, board):
            return moves  # Cannot castle while in check

        # Castling
        if not self.has_moved:
            # Kingside castling
            kingside_rook = board.get_piece((row, 7))
            if (kingside_rook and 
                isinstance(kingside_rook, Rook) and 
                kingside_rook.color == self.color and
                not kingside_rook.has_moved and
                all(board.get_piece((row, c)) is None for c in range(col + 1, 7))):
                # Check if castling squares are under attack
                if not any(self.is_square_attacked((row, c), board) for c in range(col, col + 3)):
                    moves.append((row, col + 2))

            # Queenside castling
            queenside_rook = board.get_piece((row, 0))
            if (queenside_rook and 
                isinstance(queenside_rook, Rook) and 
                queenside_rook.color == self.color and
                not queenside_rook.has_moved and
                all(board.get_piece((row, c)) is None for c in range(1, col))):
                # Check if castling squares are under attack
                if not any(self.is_square_attacked((row, c), board) for c in range(col - 2, col + 1)):
                    moves.append((row, col - 2))

        return moves 