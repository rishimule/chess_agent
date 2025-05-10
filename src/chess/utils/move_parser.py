from typing import Tuple
from ..board import Board
from ..pieces import Color

def parse_move(move_str: str, board: Board) -> tuple[tuple[int, int], tuple[int, int]]:
    """Parse a move string into board coordinates.
    
    Args:
        move_str: The move string in algebraic notation (e.g., 'e2e4')
        board: The current chess board state
        
    Returns:
        A tuple of (start_position, end_position) where each position is a tuple of (row, col)
        
    Raises:
        ValueError: If the move string format is invalid
        
    Note:
        Supports:
        - Regular moves in algebraic notation (e.g., 'e2e4')
        - Kingside castling ('O-O' or 'o-o')
        - Queenside castling ('O-O-O' or 'o-o-o')
    """
    move_str = move_str.strip().lower()
    
    # Handle castling notation
    if move_str == 'o-o':  # Kingside castling
        row = 7 if board.current_turn == Color.WHITE else 0
        return ((row, 4), (row, 6))
    elif move_str == 'o-o-o':  # Queenside castling
        row = 7 if board.current_turn == Color.WHITE else 0
        return ((row, 4), (row, 2))
    
    # Handle regular moves
    if len(move_str) != 4:
        raise ValueError("Invalid move format")
    
    # Convert file (column) from a-h to 0-7
    start_col = ord(move_str[0].lower()) - ord('a')
    end_col = ord(move_str[2].lower()) - ord('a')
    
    # Convert rank (row) from 1-8 to 0-7 (inverted)
    start_row = 8 - int(move_str[1])
    end_row = 8 - int(move_str[3])
    
    return ((start_row, start_col), (end_row, end_col)) 