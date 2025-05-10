import pytest
from src.chess.pieces.rook import Rook
from src.chess.pieces.base import Color
from src.chess.board import Board

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def white_rook():
    return Rook(Color.WHITE)

@pytest.fixture
def black_rook():
    return Rook(Color.BLACK)

def test_rook_symbols(white_rook, black_rook):
    """Test that rooks have correct Unicode and ASCII symbols"""
    assert white_rook.get_symbol() == '♖'
    assert black_rook.get_symbol() == '♜'
    assert white_rook.get_ascii_symbol() == 'R'
    assert black_rook.get_ascii_symbol() == 'r'

def test_rook_center_moves(white_rook, board):
    """Test rook's moves from center position"""
    # Place rook at d4 (3,3)
    start_pos = (3, 3)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[start_pos[0]][start_pos[1]] = white_rook
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    expected_moves = []
    # Up
    for r in range(2, -1, -1):
        expected_moves.append((r, 3))
    # Down
    for r in range(4, 8):
        expected_moves.append((r, 3))
    # Left
    for c in range(2, -1, -1):
        expected_moves.append((3, c))
    # Right
    for c in range(4, 8):
        expected_moves.append((3, c))
    assert set(valid_moves) == set(expected_moves)

def test_rook_corner_moves(white_rook, board):
    """Test rook's moves from corner position"""
    # Place rook at a1 (0,0)
    start_pos = (0, 0)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[start_pos[0]][start_pos[1]] = white_rook
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    expected_moves = []
    # Up
    for r in range(1, 8):
        expected_moves.append((r, 0))
    # Right
    for c in range(1, 8):
        expected_moves.append((0, c))
    assert set(valid_moves) == set(expected_moves)

def test_rook_edge_moves(white_rook, board):
    """Test rook's moves from edge position"""
    # Place rook at a4 (3,0)
    start_pos = (3, 0)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[start_pos[0]][start_pos[1]] = white_rook
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    expected_moves = []
    # Up
    for r in range(2, -1, -1):
        expected_moves.append((r, 0))
    # Down
    for r in range(4, 8):
        expected_moves.append((r, 0))
    # Right
    for c in range(1, 8):
        expected_moves.append((3, c))
    assert set(valid_moves) == set(expected_moves)

def test_rook_capture_moves(white_rook, black_rook, board):
    """Test rook's capture moves"""
    # Place white rook at d4 (3,3)
    start_pos = (3, 3)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[start_pos[0]][start_pos[1]] = white_rook
    # Place black pieces in capture positions
    capture_positions = [(3, 0), (3, 7), (0, 3), (7, 3)]
    for pos in capture_positions:
        board.board[pos[0]][pos[1]] = black_rook
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    # Should be able to move up to and including the first black piece in each direction
    expected_moves = []
    # Left
    for c in range(2, -1, -1):
        expected_moves.append((3, c))
    expected_moves.append((3, 0))  # Capture
    # Right
    for c in range(4, 7):
        expected_moves.append((3, c))
    expected_moves.append((3, 7))  # Capture
    # Up
    for r in range(2, 0, -1):
        expected_moves.append((r, 3))
    expected_moves.append((0, 3))  # Capture
    # Down
    for r in range(4, 7):
        expected_moves.append((r, 3))
    expected_moves.append((7, 3))  # Capture
    assert set(valid_moves) == set(expected_moves)
    # Place friendly piece in capture position
    board.board[0][3] = white_rook
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    assert (0, 3) not in valid_moves  # Cannot capture friendly piece

def test_rook_blocked_moves(white_rook, black_rook, board):
    """Test rook's moves when blocked by pieces"""
    # Place white rook at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_rook
    # Place black pieces blocking some paths
    blocking_positions = [(3, 1), (1, 3), (3, 5), (5, 3)]
    for pos in blocking_positions:
        board.board[pos[0]][pos[1]] = black_rook
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    # Should be able to capture blocking pieces
    assert all(pos in valid_moves for pos in blocking_positions)
    # Should not be able to move beyond blocking pieces
    assert (3, 0) not in valid_moves
    assert (0, 3) not in valid_moves
    assert (3, 6) not in valid_moves
    assert (6, 3) not in valid_moves

def test_rook_invalid_positions(white_rook, board):
    """Test rook's behavior with invalid positions"""
    # Test with out of bounds position
    assert len(white_rook.get_valid_moves((-1, 0), board)) == 0
    assert len(white_rook.get_valid_moves((0, 8), board)) == 0
    # Test with invalid position types
    assert len(white_rook.get_valid_moves((3.5, 3), board)) == 0
    assert len(white_rook.get_valid_moves((3, "3"), board)) == 0

def test_rook_has_moved_flag(white_rook, board):
    """Test that rook's has_moved flag is properly set"""
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_rook
    assert not white_rook.has_moved
    # Make a move
    end_pos = (3, 5)
    board.make_move(start_pos, end_pos)
    assert white_rook.has_moved

def test_rook_surrounded_by_friendly(white_rook, board):
    """Test rook has no moves when surrounded by friendly pieces"""
    # Place rook at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_rook
    # Surround with white pieces
    surrounding_positions = [
        (2, 3), (3, 2), (3, 4), (4, 3)
    ]
    for pos in surrounding_positions:
        board.board[pos[0]][pos[1]] = Rook(Color.WHITE)
    valid_moves = white_rook.get_valid_moves(start_pos, board)
    assert valid_moves == []

def test_black_rook_moves(board):
    rook = Rook(Color.BLACK)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[4][4] = rook
    valid_moves = rook.get_valid_moves((4,4), board)
    expected_moves = []
    # Up
    for r in range(3, -1, -1):
        expected_moves.append((r, 4))
    # Down
    for r in range(5, 8):
        expected_moves.append((r, 4))
    # Left
    for c in range(3, -1, -1):
        expected_moves.append((4, c))
    # Right
    for c in range(5, 8):
        expected_moves.append((4, c))
    assert set(valid_moves) == set(expected_moves) 