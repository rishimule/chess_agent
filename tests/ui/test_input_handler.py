import pytest
from unittest.mock import patch
from src.chess.board import Board
from src.chess.pieces import Color, PieceType
from src.chess.ui.input_handler import get_move_from_user, get_promotion_piece

@pytest.fixture
def board():
    return Board()

def test_get_move_regular_move(board):
    with patch('builtins.input', return_value='e2e4'):
        start_pos, end_pos = get_move_from_user(board)
        assert start_pos == (6, 4)  # e2
        assert end_pos == (4, 4)    # e4

def test_get_move_kingside_castling(board):
    with patch('builtins.input', return_value='O-O'):
        start_pos, end_pos = get_move_from_user(board)
        assert start_pos == (7, 4)  # e1
        assert end_pos == (7, 6)    # g1

def test_get_move_queenside_castling(board):
    with patch('builtins.input', return_value='O-O-O'):
        start_pos, end_pos = get_move_from_user(board)
        assert start_pos == (7, 4)  # e1
        assert end_pos == (7, 2)    # c1

def test_get_move_undo(board):
    # First make some moves to undo
    board.make_move((6, 4), (4, 4))  # e2e4
    board.make_move((1, 4), (3, 4))  # e7e5
    
    with patch('builtins.input', return_value='undo'):
        start_pos, end_pos = get_move_from_user(board)
        assert start_pos == "undo"
        assert end_pos == "undo"

def test_get_move_invalid_format(board):
    with patch('builtins.input', side_effect=['invalid', 'e2e4']):
        start_pos, end_pos = get_move_from_user(board)
        assert start_pos == (6, 4)  # e2
        assert end_pos == (4, 4)    # e4

def test_get_move_out_of_bounds(board):
    with patch('builtins.input', side_effect=['e2e9', 'e2e4']):
        start_pos, end_pos = get_move_from_user(board)
        assert start_pos == (6, 4)  # e2
        assert end_pos == (4, 4)    # e4

def test_get_promotion_piece_queen():
    with patch('builtins.input', return_value='Q'):
        piece = get_promotion_piece()
        assert piece == PieceType.QUEEN

def test_get_promotion_piece_rook():
    with patch('builtins.input', return_value='R'):
        piece = get_promotion_piece()
        assert piece == PieceType.ROOK

def test_get_promotion_piece_bishop():
    with patch('builtins.input', return_value='B'):
        piece = get_promotion_piece()
        assert piece == PieceType.BISHOP

def test_get_promotion_piece_knight():
    with patch('builtins.input', return_value='N'):
        piece = get_promotion_piece()
        assert piece == PieceType.KNIGHT

def test_get_promotion_piece_invalid_then_valid():
    with patch('builtins.input', side_effect=['X', 'Q']):
        piece = get_promotion_piece()
        assert piece == PieceType.QUEEN
