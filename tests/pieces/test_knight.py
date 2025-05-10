import pytest
from src.chess.pieces.knight import Knight
from src.chess.pieces.base import Color
from src.chess.board import Board

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def white_knight():
    return Knight(Color.WHITE)

@pytest.fixture
def black_knight():
    return Knight(Color.BLACK)

def test_knight_symbols(white_knight, black_knight):
    """Test that knights have correct Unicode and ASCII symbols"""
    assert white_knight.get_symbol() == '♘'
    assert black_knight.get_symbol() == '♞'
    assert white_knight.get_ascii_symbol() == 'N'
    assert black_knight.get_ascii_symbol() == 'n'

def test_knight_initial_moves(white_knight, board):
    """Test knight's initial moves from starting position"""
    # Place knight at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_knight
    
    valid_moves = white_knight.get_valid_moves(start_pos, board)
    expected_moves = [
        (1, 2), (1, 4),  # Up-left and up-right
        (2, 1), (2, 5),  # Left-up and right-up
        (4, 1), (4, 5),  # Left-down and right-down
        (5, 2), (5, 4)   # Down-left and down-right
    ]
    
    assert len(valid_moves) == len(expected_moves)
    assert all(move in valid_moves for move in expected_moves)

def test_knight_corner_moves(white_knight, board):
    """Test knight's moves from corner positions"""
    # Test from a1 (0,0)
    start_pos = (0, 0)
    board.board[start_pos[0]][start_pos[1]] = white_knight
    
    valid_moves = white_knight.get_valid_moves(start_pos, board)
    expected_moves = [(1, 2), (2, 1)]
    
    assert len(valid_moves) == len(expected_moves)
    assert all(move in valid_moves for move in expected_moves)

def test_knight_edge_moves(white_knight, board):
    """Test knight's moves from edge positions"""
    # Test from a4 (3,0)
    start_pos = (3, 0)
    board.board[start_pos[0]][start_pos[1]] = white_knight
    
    valid_moves = white_knight.get_valid_moves(start_pos, board)
    expected_moves = [
        (1, 1), (2, 2),  # Up-right and right-up
        (4, 2), (5, 1)   # Right-down and down-right
    ]
    
    assert len(valid_moves) == len(expected_moves)
    assert all(move in valid_moves for move in expected_moves)

def test_knight_capture_moves(white_knight, board):
    """Test knight's capture moves"""
    # Place white knight at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_knight
    
    # Place black pieces in capture positions
    capture_positions = [(1, 2), (1, 4), (2, 1), (2, 5)]
    for pos in capture_positions:
        board.board[pos[0]][pos[1]] = Knight(Color.BLACK)  # Create new instance for each position
    
    valid_moves = white_knight.get_valid_moves(start_pos, board)
    
    # Should be able to capture black pieces
    assert all(pos in valid_moves for pos in capture_positions)
    
    # Should not be able to capture own pieces
    board.board[4][1] = Knight(Color.WHITE)  # Create new white knight instance
    valid_moves = white_knight.get_valid_moves(start_pos, board)
    assert (4, 1) not in valid_moves

def test_knight_blocked_moves(white_knight, board):
    """Test knight's moves when surrounded by pieces"""
    # Place white knight at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_knight
    
    # Surround knight with black pieces
    surrounding_positions = [
        (1, 2), (1, 4), (2, 1), (2, 5),
        (4, 1), (4, 5), (5, 2), (5, 4)
    ]
    for pos in surrounding_positions:
        board.board[pos[0]][pos[1]] = Knight(Color.BLACK)  # Create new instance for each position
    
    valid_moves = white_knight.get_valid_moves(start_pos, board)
    
    # Should be able to capture all surrounding pieces
    assert len(valid_moves) == len(surrounding_positions)
    assert all(pos in valid_moves for pos in surrounding_positions)

def test_knight_invalid_positions(white_knight, board):
    """Test knight's behavior with invalid positions"""
    # Test with out of bounds position
    assert len(white_knight.get_valid_moves((-1, 0), board)) == 0
    assert len(white_knight.get_valid_moves((0, 8), board)) == 0
    
    # Test with invalid position types
    assert len(white_knight.get_valid_moves((3.5, 3), board)) == 0
    assert len(white_knight.get_valid_moves((3, "3"), board)) == 0

def test_knight_has_moved_flag(white_knight, board):
    """Test that knight's has_moved flag is properly set"""
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_knight
    
    assert not white_knight.has_moved
    
    # Make a move
    end_pos = (1, 2)
    board.make_move(start_pos, end_pos)
    
    assert white_knight.has_moved

def test_knight_surrounded_by_friendly(board):
    knight = Knight(Color.WHITE)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[3][3] = knight
    # All knight moves
    moves = [
        (1, 2), (1, 4), (2, 1), (2, 5),
        (4, 1), (4, 5), (5, 2), (5, 4)
    ]
    for pos in moves:
        board.board[pos[0]][pos[1]] = Knight(Color.WHITE)
    valid_moves = knight.get_valid_moves((3,3), board)
    assert valid_moves == []

def test_black_knight_moves(board):
    knight = Knight(Color.BLACK)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[4][4] = knight
    valid_moves = knight.get_valid_moves((4,4), board)
    expected_moves = [
        (2, 3), (2, 5), (3, 2), (3, 6),
        (5, 2), (5, 6), (6, 3), (6, 5)
    ]
    assert set(valid_moves) == set(expected_moves) 