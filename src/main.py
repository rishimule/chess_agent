from chess.board import Board
from chess.pieces import Color, PieceType, Pawn
from chess.engines import MinimaxEngine
from chess.ui import print_board, get_move_from_user, get_promotion_piece

def main():
    """Main function to run the chess game.
    
    This function:
    1. Initializes the chess board and AI engine
    2. Runs the main game loop until a terminal condition is reached
    3. Handles player moves and AI moves
    4. Checks for game over conditions:
       - Checkmate
       - Stalemate
       - Threefold repetition
       - Fifty-move rule
       - Insufficient material
    5. Manages pawn promotion
    6. Displays the board state and game status
    
    The player plays as White against the AI (Black).
    The AI uses the MinimaxEngine with alpha-beta pruning.
    """
    board = Board()
    ai = MinimaxEngine(depth=3)  # Adjust depth for AI difficulty
    
    print("Welcome to Chess AI!")
    print("You are playing as White.")
    
    while True:
        print_board(board)
        
        # Check for game over conditions
        if board.is_checkmate(board.current_turn):
            winner = "Black" if board.current_turn == Color.WHITE else "White"
            print(f"Checkmate! {winner} wins!")
            break
        elif board.is_stalemate():
            print("Stalemate! The game is a draw.")
            break
        elif board.is_threefold_repetition():
            print("Draw by threefold repetition!")
            break
        elif board.is_fifty_moves():
            print("Draw by fifty-move rule!")
            break
        elif board.is_insufficient_material():
            print("Draw by insufficient material!")
            break
        
        # Display check warning
        if board.is_check(board.current_turn):
            print(f"{'White' if board.current_turn == Color.WHITE else 'Black'} is in check!")
        
        # Player's turn
        if board.current_turn == Color.WHITE:
            while True:
                try:
                    start_pos, end_pos = get_move_from_user(board)
                    
                    # Handle undo
                    if start_pos == "undo" and end_pos == "undo":
                        print_board(board)
                        continue
                    
                    # Check for pawn promotion
                    piece = board.get_piece(start_pos)
                    promotion_piece = None
                    if (isinstance(piece, Pawn) and
                        ((board.current_turn == Color.WHITE and end_pos[0] == 0) or
                         (board.current_turn == Color.BLACK and end_pos[0] == 7))):
                        promotion_piece = get_promotion_piece()

                    # Make the move
                    if not board.make_move(start_pos, end_pos, promotion_piece):
                        print("Invalid move! Try again.")
                        continue
                    break
                except ValueError as e:
                    print(str(e))
        # AI's turn
        else:
            print("AI is thinking...")
            move = ai.get_best_move(board)
            if move:
                start_pos, end_pos = move
                # AI always promotes to queen
                piece = board.get_piece(start_pos)
                if (piece and isinstance(piece, Pawn) and 
                    (end_pos[0] == 0 or end_pos[0] == 7)):
                    board.make_move(start_pos, end_pos, PieceType.QUEEN)
                else:
                    board.make_move(start_pos, end_pos)
                # Convert coordinates to algebraic notation
                start_file = chr(start_pos[1] + ord('a'))
                start_rank = str(8 - start_pos[0])
                end_file = chr(end_pos[1] + ord('a'))
                end_rank = str(8 - end_pos[0])
                print(f"AI played: {start_file}{start_rank}{end_file}{end_rank}")
            else:
                print("AI couldn't find a valid move!")
                break

if __name__ == "__main__":
    main() 