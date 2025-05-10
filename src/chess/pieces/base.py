from enum import Enum
from typing import List, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..board import Board

class Color(Enum):
    WHITE = 1
    BLACK = 2

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Piece:
    def __init__(self, color: Color):
        self.color = color
        self.has_moved = False

    def get_symbol(self) -> str:
        """Get the Unicode symbol for the piece."""
        raise NotImplementedError

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the piece."""
        raise NotImplementedError

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for this piece from the given position."""
        raise NotImplementedError

    def is_valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], board: 'Board') -> bool:
        """Check if a move is valid."""
        return end_pos in self.get_valid_moves(start_pos, board) 