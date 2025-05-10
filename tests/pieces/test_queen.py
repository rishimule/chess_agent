import pytest
from src.chess.pieces.queen import Queen
from src.chess.pieces.base import Color
from src.chess.board import Board

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def white_queen():
    return Queen(Color.WHITE)

@pytest.fixture
def black_queen():
    return Queen(Color.BLACK)

def test_queen_symbols(white_queen, black_queen):
    """Test that queens have correct Unicode and ASCII symbols"""
    assert white_queen.get_symbol() == '♕'
    assert black_queen.get_symbol() == '♛'
    assert white_queen.get_ascii_symbol() == 'Q'
    assert black_queen.get_ascii_symbol() == 'q'

def test_queen_center_moves(white_queen, board):
    """Test queen's moves from center position"""
    # Place queen at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    
    # Should be able to move in all 8 directions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Up-left, Up, Up-right
        (0, -1),           (0, 1),   # Left, Right
        (1, -1),  (1, 0),  (1, 1)    # Down-left, Down, Down-right
    ]
    
    # Check first move in each direction
    for drow, dcol in directions:
        expected_move = (start_pos[0] + drow, start_pos[1] + dcol)
        assert expected_move in valid_moves

def test_queen_corner_moves(white_queen, board):
    """Test queen's moves from corner position"""
    # Place queen at a1 (0,0)
    start_pos = (0, 0)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    
    # Should only be able to move right, up-right, and up
    expected_directions = [(0, 1), (1, 1), (1, 0)]
    for drow, dcol in expected_directions:
        expected_move = (start_pos[0] + drow, start_pos[1] + dcol)
        assert expected_move in valid_moves
    
    # Should not be able to move in other directions
    invalid_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1)]
    for drow, dcol in invalid_directions:
        invalid_move = (start_pos[0] + drow, start_pos[1] + dcol)
        assert invalid_move not in valid_moves

def test_queen_edge_moves(white_queen, board):
    """Test queen's moves from edge position"""
    # Place queen at a4 (3,0)
    start_pos = (3, 0)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    
    # Should be able to move right, up-right, down-right, up, and down
    expected_directions = [(0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0)]
    for drow, dcol in expected_directions:
        expected_move = (start_pos[0] + drow, start_pos[1] + dcol)
        assert expected_move in valid_moves
    
    # Should not be able to move left
    invalid_directions = [(-1, -1), (0, -1), (1, -1)]
    for drow, dcol in invalid_directions:
        invalid_move = (start_pos[0] + drow, start_pos[1] + dcol)
        assert invalid_move not in valid_moves

def test_queen_capture_moves(white_queen, black_queen, board):
    """Test queen's capture moves"""
    # Place white queen at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    
    # Place black pieces in capture positions
    capture_positions = [
        (1, 1), (1, 3), (1, 5),  # Diagonal and vertical
        (3, 1), (3, 5),          # Horizontal
        (5, 1), (5, 3), (5, 5)   # Diagonal and vertical
    ]
    for pos in capture_positions:
        board.board[pos[0]][pos[1]] = black_queen
    
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    
    # Should be able to capture all black pieces
    assert all(pos in valid_moves for pos in capture_positions)
    
    # Place friendly piece in capture position
    board.board[1][1] = white_queen
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    assert (1, 1) not in valid_moves  # Cannot capture friendly piece

def test_queen_blocked_moves(white_queen, black_queen, board):
    """Test queen's moves when blocked by pieces"""
    # Place white queen at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    
    # Place black pieces blocking some paths
    blocking_positions = [
        (1, 1),  # Diagonal up-left
        (3, 1),  # Horizontal left
        (5, 5)   # Diagonal down-right
    ]
    for pos in blocking_positions:
        board.board[pos[0]][pos[1]] = black_queen
    
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    
    # Should be able to capture blocking pieces
    assert all(pos in valid_moves for pos in blocking_positions)
    
    # Should not be able to move beyond blocking pieces
    assert (0, 0) not in valid_moves  # Beyond up-left block
    assert (3, 0) not in valid_moves  # Beyond left block
    assert (6, 6) not in valid_moves  # Beyond down-right block

def test_queen_invalid_positions(white_queen, board):
    """Test queen's behavior with invalid positions"""
    # Test with out of bounds position
    assert len(white_queen.get_valid_moves((-1, 0), board)) == 0
    assert len(white_queen.get_valid_moves((0, 8), board)) == 0
    
    # Test with invalid position types
    assert len(white_queen.get_valid_moves((3.5, 3), board)) == 0
    assert len(white_queen.get_valid_moves((3, "3"), board)) == 0

def test_queen_has_moved_flag(white_queen, board):
    """Test that queen's has_moved flag is properly set"""
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    
    assert not white_queen.has_moved
    
    # Make a move
    end_pos = (4, 4)
    board.make_move(start_pos, end_pos)
    
    assert white_queen.has_moved

def test_queen_surrounded_by_friendly(white_queen, board):
    """Test queen has no moves when surrounded by friendly pieces"""
    # Place queen at d4 (3,3)
    start_pos = (3, 3)
    board.board[start_pos[0]][start_pos[1]] = white_queen
    # Surround with white pieces
    surrounding_positions = [
        (2, 2), (2, 3), (2, 4),
        (3, 2),         (3, 4),
        (4, 2), (4, 3), (4, 4)
    ]
    for pos in surrounding_positions:
        board.board[pos[0]][pos[1]] = Queen(Color.WHITE)
    valid_moves = white_queen.get_valid_moves(start_pos, board)
    assert valid_moves == [] 