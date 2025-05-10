import pytest
from src.chess.board import Board
from src.chess.pieces import Color
from src.chess.utils.move_parser import parse_move

@pytest.fixture
def board():
    return Board()

def test_parse_regular_move(board):
    move_str = "e2e4"
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (6, 4)  # e2
    assert end_pos == (4, 4)    # e4

def test_parse_kingside_castling(board):
    move_str = "O-O"
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (7, 4)  # e1
    assert end_pos == (7, 6)    # g1

def test_parse_queenside_castling(board):
    move_str = "O-O-O"
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (7, 4)  # e1
    assert end_pos == (7, 2)    # c1

def test_parse_move_case_insensitive(board):
    move_str = "E2E4"
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (6, 4)  # e2
    assert end_pos == (4, 4)    # e4

def test_parse_move_with_spaces(board):
    move_str = " e2e4 "
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (6, 4)  # e2
    assert end_pos == (4, 4)    # e4

def test_parse_invalid_move_format():
    board = Board()
    with pytest.raises(ValueError):
        parse_move("invalid", board)

def test_parse_move_black_turn(board):
    board.current_turn = Color.BLACK
    move_str = "e7e5"
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (1, 4)  # e7
    assert end_pos == (3, 4)    # e5

def test_parse_castling_black_turn(board):
    board.current_turn = Color.BLACK
    move_str = "O-O"
    start_pos, end_pos = parse_move(move_str, board)
    assert start_pos == (0, 4)  # e8
    assert end_pos == (0, 6)    # g8 