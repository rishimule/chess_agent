import pytest
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.base import Color
from src.chess.board import Board

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def white_pawn():
    return Pawn(Color.WHITE)

@pytest.fixture
def black_pawn():
    return Pawn(Color.BLACK)

def test_pawn_symbols(white_pawn, black_pawn):
    """Test that pawns have correct Unicode and ASCII symbols"""
    assert white_pawn.get_symbol() == '♙'
    assert black_pawn.get_symbol() == '♟'
    assert white_pawn.get_ascii_symbol() == 'P'
    assert black_pawn.get_ascii_symbol() == 'p'

def test_white_pawn_initial_moves(white_pawn, board):
    """Test white pawn's initial moves"""
    # Place pawn at starting position (e2)
    start_pos = (6, 4)  # Second rank from bottom
    board.board[start_pos[0]][start_pos[1]] = white_pawn
    
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    expected_moves = [
        (5, 4),  # One square forward
        (4, 4)   # Two squares forward
    ]
    
    assert len(valid_moves) == len(expected_moves)
    assert all(move in valid_moves for move in expected_moves)

def test_black_pawn_initial_moves(black_pawn, board):
    """Test black pawn's initial moves"""
    # Place pawn at starting position (e7)
    start_pos = (1, 4)  # Second rank from top
    board.board[start_pos[0]][start_pos[1]] = black_pawn
    
    valid_moves = black_pawn.get_valid_moves(start_pos, board)
    expected_moves = [
        (2, 4),  # One square forward
        (3, 4)   # Two squares forward
    ]
    
    assert len(valid_moves) == len(expected_moves)
    assert all(move in valid_moves for move in expected_moves)

def test_pawn_blocked_moves(white_pawn, black_pawn, board):
    """Test pawn's moves when blocked"""
    # Place white pawn
    white_pos = (6, 4)
    board.board[white_pos[0]][white_pos[1]] = white_pawn
    
    # Place blocking piece one square ahead
    board.board[5][4] = Pawn(Color.BLACK)
    
    valid_moves = white_pawn.get_valid_moves(white_pos, board)
    assert len(valid_moves) == 0  # Should have no valid moves when blocked
    
    # Place black pawn with white pawn blocking two squares ahead
    black_pos = (1, 4)
    board.board[black_pos[0]][black_pos[1]] = black_pawn
    board.board[3][4] = Pawn(Color.WHITE)
    
    valid_moves = black_pawn.get_valid_moves(black_pos, board)
    assert (2, 4) in valid_moves  # Can move one square
    assert (3, 4) not in valid_moves  # Cannot move two squares (blocked)

def test_pawn_capture_moves(white_pawn, board):
    """Test pawn's diagonal capture moves"""
    # Place white pawn at e4
    start_pos = (4, 4)
    board.board[start_pos[0]][start_pos[1]] = white_pawn
    
    # Place black pawns in capture positions
    board.board[3][3] = Pawn(Color.BLACK)  # Diagonal left
    board.board[3][5] = Pawn(Color.BLACK)  # Diagonal right
    
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    expected_captures = [(3, 3), (3, 5)]
    
    assert all(move in valid_moves for move in expected_captures)
    assert (3, 4) in valid_moves  # Can still move forward
    
    # Place friendly piece in capture position
    board.board[3][3] = Pawn(Color.WHITE)
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (3, 3) not in valid_moves  # Cannot capture friendly piece

def test_pawn_edge_moves(white_pawn, black_pawn, board):
    """Test pawn's moves at the edge of the board"""
    # Test white pawn at a2
    white_pos = (6, 0)
    board.board[white_pos[0]][white_pos[1]] = white_pawn
    
    valid_moves = white_pawn.get_valid_moves(white_pos, board)
    assert (5, 0) in valid_moves  # One square forward
    assert (4, 0) in valid_moves  # Two squares forward
    
    # Test black pawn at h7
    black_pos = (1, 7)
    board.board[black_pos[0]][black_pos[1]] = black_pawn
    
    valid_moves = black_pawn.get_valid_moves(black_pos, board)
    assert (2, 7) in valid_moves  # One square forward
    assert (3, 7) in valid_moves  # Two squares forward

def test_pawn_en_passant(white_pawn, board):
    """Test en passant capture"""
    # Place white pawn at e5
    start_pos = (3, 4)
    board.board[start_pos[0]][start_pos[1]] = white_pawn
    white_pawn.has_moved = True  # Pawn has moved from initial position
    
    # Set up en passant target (as if black pawn just moved from f7 to f5)
    board.en_passant_target = (2, 5)
    
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (2, 5) in valid_moves  # Should be able to capture en passant

def test_pawn_invalid_positions(white_pawn, board):
    """Test pawn's behavior with invalid positions"""
    # Test with out of bounds position
    assert len(white_pawn.get_valid_moves((-1, 0), board)) == 0
    assert len(white_pawn.get_valid_moves((0, 8), board)) == 0
    
    # Test with invalid position types
    assert len(white_pawn.get_valid_moves((3.5, 3), board)) == 0
    assert len(white_pawn.get_valid_moves((3, "3"), board)) == 0

def test_pawn_has_moved_flag(white_pawn, board):
    """Test that pawn's has_moved flag affects available moves"""
    # Place pawn at starting position
    start_pos = (6, 4)
    board.board[start_pos[0]][start_pos[1]] = white_pawn
    
    # Initially should be able to move two squares
    assert not white_pawn.has_moved
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (4, 4) in valid_moves  # Two squares forward
    
    # After moving, should not be able to move two squares
    white_pawn.has_moved = True
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (4, 4) not in valid_moves  # Cannot move two squares
    assert (5, 4) in valid_moves  # Can still move one square

def test_pawn_promotion(white_pawn, black_pawn, board):
    """Test that pawns can't move forward at the last rank"""
    # Test white pawn at last rank
    white_pos = (0, 4)
    board.board[white_pos[0]][white_pos[1]] = white_pawn
    valid_moves = white_pawn.get_valid_moves(white_pos, board)
    assert len(valid_moves) == 0  # Should have no valid moves at last rank
    
    # Test black pawn at last rank
    black_pos = (7, 4)
    board.board[black_pos[0]][black_pos[1]] = black_pawn
    valid_moves = black_pawn.get_valid_moves(black_pos, board)
    assert len(valid_moves) == 0  # Should have no valid moves at last rank

def test_pawn_en_passant_edge_cases(white_pawn, board):
    """Test edge cases for en passant capture"""
    # Place white pawn at e5
    start_pos = (3, 4)
    board.board[start_pos[0]][start_pos[1]] = white_pawn
    white_pawn.has_moved = True
    
    # Test en passant target not set
    board.en_passant_target = None
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (2, 5) not in valid_moves  # Should not be able to capture en passant
    
    # Test en passant target not adjacent
    board.en_passant_target = (2, 6)  # Not adjacent to pawn
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (2, 6) not in valid_moves  # Should not be able to capture en passant

def test_pawn_capture_edge_cases(white_pawn, black_pawn, board):
    """Test edge cases for pawn captures"""
    # Test white pawn at a4 with black pawn at b3
    white_pos = (4, 0)
    board.board[white_pos[0]][white_pos[1]] = white_pawn
    board.board[3][1] = Pawn(Color.BLACK)
    
    valid_moves = white_pawn.get_valid_moves(white_pos, board)
    assert (3, 1) in valid_moves  # Can capture right
    assert (3, -1) not in valid_moves  # Cannot capture left (off board)
    
    # Test black pawn at h4 with white pawn at g3
    black_pos = (3, 7)
    board.board[black_pos[0]][black_pos[1]] = black_pawn
    board.board[4][6] = Pawn(Color.WHITE)
    
    valid_moves = black_pawn.get_valid_moves(black_pos, board)
    assert (4, 6) in valid_moves  # Can capture left
    assert (4, 8) not in valid_moves  # Cannot capture right (off board)

def test_pawn_promotion_mechanism(white_pawn, board):
    """Test that pawn can reach last rank and is eligible for promotion (placeholder if not implemented)"""
    start_pos = (1, 4)
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[start_pos[0]][start_pos[1]] = white_pawn
    white_pawn.has_moved = True
    valid_moves = white_pawn.get_valid_moves(start_pos, board)
    assert (0, 4) in valid_moves  # Pawn can move to last rank
    # If promotion is implemented, check promotion logic here
    # Example: assert board.promote_pawn((0, 4), ...) or similar 