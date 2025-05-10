from typing import Tuple
from ..board import Board
from ..pieces import Color, PieceType, Pawn
from ..utils.move_parser import parse_move

def get_move_from_user(board: Board) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Get a move from the user through the console.
    
    Args:
        board: The current chess board state
        
    Returns:
        A tuple of (start_position, end_position) where each position is a tuple of (row, col)
        Special return value ("undo", "undo") if the user requests to undo moves
        
    Note:
        Handles:
        - Regular moves in algebraic notation (e.g., 'e2e4')
        - Castling moves ('O-O' or 'O-O-O')
        - Move undo requests ('undo')
        - Input validation and error messages
    """
    while True:
        move = input("Enter your move (e.g., 'e2e4', 'O-O' for kingside castling, 'O-O-O' for queenside castling, or 'undo' to take back last move): ").strip().lower()
        
        # Handle undo
        if move == "undo":
            # Need to undo both player's and AI's last moves
            if board.undo_move() and board.undo_move():
                return "undo", "undo"  # Special return value to indicate undo
            else:
                print("Cannot undo any more moves!")
                continue
        
        # Handle castling
        if move == "o-o" or move == "0-0":  # Kingside castling
            if board.current_turn == Color.WHITE:
                return (7, 4), (7, 6)
            else:
                return (0, 4), (0, 6)
        elif move == "o-o-o" or move == "0-0-0":  # Queenside castling
            if board.current_turn == Color.WHITE:
                return (7, 4), (7, 2)
            else:
                return (0, 4), (0, 2)

        # Handle regular moves
        if len(move) != 4:
            print("Invalid move format. Please use algebraic notation (e.g., 'e2e4')")
            continue

        try:
            start_col = ord(move[0]) - ord('a')
            start_row = 8 - int(move[1])
            end_col = ord(move[2]) - ord('a')
            end_row = 8 - int(move[3])

            if not (0 <= start_row < 8 and 0 <= start_col < 8 and
                   0 <= end_row < 8 and 0 <= end_col < 8):
                print("Move is out of bounds")
                continue

            return (start_row, start_col), (end_row, end_col)
        except ValueError:
            print("Invalid move format. Please use algebraic notation (e.g., 'e2e4')")

def get_promotion_piece() -> PieceType:
    """Get the piece type for pawn promotion from the user.
    
    Returns:
        A PieceType enum value representing the chosen promotion piece
        
    Note:
        Prompts the user to choose between:
        - Q: Queen (default)
        - R: Rook
        - B: Bishop
        - N: Knight
        
        Continues prompting until a valid choice is made.
    """
    while True:
        choice = input("Choose promotion piece (Q/R/B/N): ").strip().upper()
        if choice == 'Q':
            return PieceType.QUEEN
        elif choice == 'R':
            return PieceType.ROOK
        elif choice == 'B':
            return PieceType.BISHOP
        elif choice == 'N':
            return PieceType.KNIGHT
        print("Invalid choice. Please choose Q (Queen), R (Rook), B (Bishop), or N (Knight)") 