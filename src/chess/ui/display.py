from ..board import Board

def print_board(board: Board):
    """Print the chess board in a readable format.
    
    Args:
        board: The current chess board state
        
    The board is printed with:
    - Column labels (a-h) at the top and bottom
    - Row numbers (8-1) on the left and right
    - Pieces represented by their Unicode symbols
    - Empty squares represented by dots
    - Separator lines for better readability
    """
    print("\n  a b c d e f g h")
    print("  ---------------")
    for i in range(8):
        row = f"{8-i} "
        for j in range(8):
            piece = board.get_piece((i, j))
            if piece is None:
                row += ". "
            else:
                row += piece.get_symbol() + " "
        print(row + f" {8-i}")
    print("  ---------------")
    print("  a b c d e f g h\n") 