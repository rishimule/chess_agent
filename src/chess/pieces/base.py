from enum import Enum
from typing import List, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..board import Board

class Color(Enum):
    """Enum representing the color of a chess piece.
    
    Attributes:
        WHITE: Represents the white pieces
        BLACK: Represents the black pieces
    """
    WHITE = 1
    BLACK = 2

class PieceType(Enum):
    """Enum representing the type of a chess piece.
    
    Attributes:
        PAWN: Represents a pawn
        KNIGHT: Represents a knight
        BISHOP: Represents a bishop
        ROOK: Represents a rook
        QUEEN: Represents a queen
        KING: Represents a king
    """
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Piece:
    """Base class for all chess pieces.
    
    This abstract class defines the interface that all chess pieces must implement.
    It provides common functionality and attributes shared by all pieces.
    
    Attributes:
        color: The color of the piece (WHITE or BLACK)
        has_moved: Whether the piece has moved from its initial position
    """
    
    def __init__(self, color: Color):
        """Initialize a new chess piece.
        
        Args:
            color: The color of the piece (WHITE or BLACK)
        """
        self.color = color
        self.has_moved = False

    def get_symbol(self) -> str:
        """Get the Unicode symbol for the piece.
        
        Returns:
            A string containing the Unicode symbol representing the piece.
            The symbol varies based on the piece's color.
            
        Note:
            This method must be implemented by all subclasses.
        """
        raise NotImplementedError

    def get_ascii_symbol(self) -> str:
        """Get the ASCII symbol for the piece.
        
        Returns:
            A string containing the ASCII symbol representing the piece.
            The symbol varies based on the piece's color.
            - White pieces use uppercase letters (P, N, B, R, Q, K)
            - Black pieces use lowercase letters (p, n, b, r, q, k)
            
        Note:
            This method must be implemented by all subclasses.
        """
        raise NotImplementedError

    def get_valid_moves(self, start_pos: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
        """Get all valid moves for this piece from the given position.
        
        Args:
            start_pos: The current position of the piece (row, col)
            board: The current state of the chess board
            
        Returns:
            A list of valid moves, where each move is a tuple of (row, col)
            representing the destination square.
            
        Note:
            This method must be implemented by all subclasses.
            The returned moves should be legal according to chess rules,
            but may not account for moves that would leave the king in check.
        """
        raise NotImplementedError

    def is_valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], board: 'Board') -> bool:
        """Check if a move is valid for this piece.
        
        Args:
            start_pos: The current position of the piece (row, col)
            end_pos: The destination position (row, col)
            board: The current state of the chess board
            
        Returns:
            True if the move is valid according to the piece's movement rules,
            False otherwise.
            
        Note:
            This method checks if the move is valid according to the piece's
            movement rules, but does not check if the move would leave the
            king in check. That check is performed by the Board class.
        """
        return end_pos in self.get_valid_moves(start_pos, board) 