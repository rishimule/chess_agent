import pytest
from io import StringIO
import sys
from src.chess.board import Board
from src.chess.pieces import Color, PieceType
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.rook import Rook
from src.chess.pieces.knight import Knight
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.queen import Queen
from src.chess.pieces.king import King
from src.chess.ui.display import print_board

@pytest.fixture
def board():
    return Board()

def test_print_empty_board(board):
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    # Print the board
    print_board(board)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Get the output
    output = captured_output.getvalue()
    
    # Check the output format
    lines = output.strip().split('\n')
    assert len(lines) == 12  # 8 rows + 2 borders + 2 column labels
    assert lines[0].strip() == "a b c d e f g h"
    assert lines[1].strip() == "---------------"
    assert lines[-2].strip() == "---------------"
    assert lines[-1].strip() == "a b c d e f g h"
    
    # Check that all squares are empty (represented by dots)
    for i in range(2, 10):
        row = lines[i].strip()
        row_num = 10 - i  # Correct mapping: i=2->8, i=3->7, ..., i=9->1
        assert row.startswith(str(row_num) + " ")
        assert row.endswith(" " + str(row_num))
        assert all(c in ". " for c in row[2:-2])

def test_print_initial_board(board):
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    # Print the board
    print_board(board)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Get the output
    output = captured_output.getvalue()
    
    # Check the output format
    lines = output.strip().split('\n')
    assert len(lines) == 12
    
    # Check that the pieces are in their initial positions
    # Black pieces (top row)
    assert "♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜" in lines[2]  # Black pieces
    assert "♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟" in lines[3]  # Black pawns
    assert "♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙" in lines[8]  # White pawns
    assert "♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖" in lines[9]  # White pieces

def test_print_custom_position(board):
    # Set up a custom position
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[0][0] = Rook(Color.WHITE)
    board.board[7][7] = King(Color.BLACK)
    board.board[3][3] = Queen(Color.WHITE)
    
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    # Print the board
    print_board(board)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Get the output
    output = captured_output.getvalue()
    
    # Check that the pieces are in their correct positions
    lines = output.strip().split('\n')
    assert "♖ . . . . . . ." in lines[2]  # White rook
    assert ". . . . . . . ♚" in lines[9]  # Black king
    assert ". . . ♕ . . . ." in lines[5]  # White queen
