import pytest
from src.chess.pieces.king import King
from src.chess.pieces.base import Color
from src.chess.board import Board
from src.chess.pieces.rook import Rook
from src.chess.pieces.pawn import Pawn

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def white_king():
    return King(Color.WHITE)

@pytest.fixture
def black_king():
    return King(Color.BLACK)

def test_symbols(white_king, black_king):
    """Test king symbols"""
    assert white_king.get_symbol() == '♔'
    assert black_king.get_symbol() == '♚'
    assert white_king.get_ascii_symbol() == 'K'
    assert black_king.get_ascii_symbol() == 'k'

def test_initial_moves(white_king, board):
    """Test king moves from starting position"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at e1 and surrounding pieces
    board.board[7][4] = white_king  # King at e1
    board.board[7][3] = King(Color.WHITE)  # Queen at d1
    board.board[7][5] = King(Color.WHITE)  # Bishop at f1
    board.board[6][3] = Pawn(Color.WHITE)  # Pawn at d2
    board.board[6][4] = Pawn(Color.WHITE)  # Pawn at e2
    board.board[6][5] = Pawn(Color.WHITE)  # Pawn at f2
    
    moves = white_king.get_valid_moves((7, 4), board)
    
    # Should have no moves initially due to surrounding pieces
    assert len(moves) == 0

def test_regular_moves(white_king, board):
    """Test king's regular movement in all directions"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at d4
    board.board[4][3] = white_king
    
    moves = set(white_king.get_valid_moves((4, 3), board))
    expected_moves = {
        (3, 2), (3, 3), (3, 4),  # North moves
        (4, 2), (4, 4),          # East-West moves
        (5, 2), (5, 3), (5, 4)   # South moves
    }
    
    assert moves == expected_moves, f"\nMissing moves: {expected_moves - moves}\nUnexpected moves: {moves - expected_moves}"

def test_capture_moves(white_king, black_king, board):
    """Test king capture moves"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at d4
    board.board[4][3] = white_king
    
    # Place black pieces in capture positions
    board.board[3][2] = black_king  # Northwest
    board.board[3][4] = black_king  # Northeast
    board.board[4][2] = black_king  # West
    board.board[4][4] = black_king  # East
    board.board[5][2] = black_king  # Southwest
    board.board[5][3] = black_king  # South
    board.board[5][4] = black_king  # Southeast
    
    moves = set(white_king.get_valid_moves((4, 3), board))
    capture_moves = {(3, 2), (3, 4), (4, 2), (4, 4), (5, 2), (5, 3), (5, 4)}
    
    # Should be able to capture all black pieces
    assert capture_moves.issubset(moves), f"Missing capture moves: {capture_moves - moves}"

def test_blocked_moves(white_king, board):
    """Test king moves when blocked by pieces"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at d4
    board.board[4][3] = white_king
    
    # Place white pieces blocking the king
    board.board[3][2] = King(Color.WHITE)  # Northwest
    board.board[3][3] = King(Color.WHITE)  # North
    board.board[3][4] = King(Color.WHITE)  # Northeast
    board.board[4][2] = King(Color.WHITE)  # West
    board.board[4][4] = King(Color.WHITE)  # East
    board.board[5][2] = King(Color.WHITE)  # Southwest
    board.board[5][3] = King(Color.WHITE)  # South
    board.board[5][4] = King(Color.WHITE)  # Southeast
    
    moves = white_king.get_valid_moves((4, 3), board)
    
    # Should have no moves when blocked by own pieces
    assert len(moves) == 0, f"Expected no moves, but got moves: {moves}"

def test_edge_positions(white_king, board):
    """Test king moves from various edge positions"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Test cases for edge positions
    edge_positions = {
        (0, 0): {(0, 1), (1, 0), (1, 1)},           # Top-left corner
        (0, 7): {(0, 6), (1, 6), (1, 7)},           # Top-right corner
        (7, 0): {(6, 0), (6, 1), (7, 1)},           # Bottom-left corner
        (7, 7): {(6, 6), (6, 7), (7, 6)},           # Bottom-right corner
        (0, 3): {(0, 2), (0, 4), (1, 2), (1, 3), (1, 4)},  # Top edge
        (7, 3): {(6, 2), (6, 3), (6, 4), (7, 2), (7, 4)},  # Bottom edge
        (3, 0): {(2, 0), (2, 1), (3, 1), (4, 0), (4, 1)},  # Left edge
        (3, 7): {(2, 6), (2, 7), (3, 6), (4, 6), (4, 7)}   # Right edge
    }
    
    for pos, expected_moves in edge_positions.items():
        # Reset board and place king
        board.board = [[None for _ in range(8)] for _ in range(8)]
        board.board[pos[0]][pos[1]] = white_king
        
        moves = set(white_king.get_valid_moves(pos, board))
        assert moves == expected_moves, f"\nTesting position {pos}:\nMissing moves: {expected_moves - moves}\nUnexpected moves: {moves - expected_moves}"

def test_castling(white_king, board):
    """Test king's castling moves"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at e1
    board.board[7][4] = white_king
    
    # Place rooks for castling
    board.board[7][0] = Rook(Color.WHITE)  # Queenside rook
    board.board[7][7] = Rook(Color.WHITE)  # Kingside rook
    
    moves = set(white_king.get_valid_moves((7, 4), board))
    expected_moves = {
        (7, 2),  # Queenside castling
        (7, 6)   # Kingside castling
    }
    
    # Should be able to castle both sides
    assert expected_moves.issubset(moves), f"Missing castling moves: {expected_moves - moves}"

def test_castling_blocked(white_king, board):
    """Test that castling is blocked when pieces are in between"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at e1
    board.board[7][4] = white_king
    
    # Place rooks for castling
    board.board[7][0] = Rook(Color.WHITE)  # Queenside rook
    board.board[7][7] = Rook(Color.WHITE)  # Kingside rook
    
    # Block castling paths
    board.board[7][1] = King(Color.WHITE)  # Block queenside
    board.board[7][6] = King(Color.WHITE)  # Block kingside
    
    moves = set(white_king.get_valid_moves((7, 4), board))
    castling_moves = {(7, 2), (7, 6)}
    
    # Should not be able to castle when blocked
    assert not any(move in moves for move in castling_moves), "Castling should be blocked when pieces are in between"

def test_castling_after_movement(white_king, board):
    """Test that castling is not allowed after king or rook has moved"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at e1
    board.board[7][4] = white_king
    
    # Place rooks for castling
    kingside_rook = Rook(Color.WHITE)
    queenside_rook = Rook(Color.WHITE)
    board.board[7][0] = queenside_rook
    board.board[7][7] = kingside_rook
    
    # Test after king has moved
    white_king.has_moved = True
    moves = set(white_king.get_valid_moves((7, 4), board))
    castling_moves = {(7, 2), (7, 6)}
    assert not any(move in moves for move in castling_moves), "Castling should not be allowed after king has moved"
    
    # Reset king's move flag and test after rooks have moved
    white_king.has_moved = False
    queenside_rook.has_moved = True
    kingside_rook.has_moved = True
    
    moves = set(white_king.get_valid_moves((7, 4), board))
    assert not any(move in moves for move in castling_moves), "Castling should not be allowed after rooks have moved"

def test_castling_through_check(white_king, black_king, board):
    """Test that castling through attacked squares is not allowed"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at e1
    board.board[7][4] = white_king
    
    # Place rooks for castling
    board.board[7][0] = Rook(Color.WHITE)
    board.board[7][7] = Rook(Color.WHITE)
    
    # Place enemy pieces attacking castling paths
    board.board[6][5] = black_king  # Attacks f1 (kingside path)
    board.board[6][3] = black_king  # Attacks d1 (queenside path)
    
    moves = set(white_king.get_valid_moves((7, 4), board))
    castling_moves = {(7, 2), (7, 6)}
    
    assert not any(move in moves for move in castling_moves), "Castling should not be allowed through attacked squares"

def test_castling_in_check(white_king, black_king, board):
    """Test that castling is not allowed while in check"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white king at e1
    board.board[7][4] = white_king
    
    # Place rooks for castling
    board.board[7][0] = Rook(Color.WHITE)
    board.board[7][7] = Rook(Color.WHITE)
    
    # Place enemy piece giving check
    board.board[6][4] = black_king  # Attacks e1 (king's position)
    
    moves = set(white_king.get_valid_moves((7, 4), board))
    castling_moves = {(7, 2), (7, 6)}
    
    assert not any(move in moves for move in castling_moves), "Castling should not be allowed while in check"

def test_invalid_positions(white_king, board):
    """Test that invalid positions return empty move list"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place a king on the board to ensure it's not affecting invalid position checks
    board.board[4][3] = white_king
    
    # Test cases for invalid positions
    invalid_positions = [
        # Out of bounds rows
        (-1, 4), (8, 4), (-100, 4), (100, 4),
        
        # Out of bounds columns
        (4, -1), (4, 8), (4, -100), (4, 100),
        
        # Out of bounds both
        (-1, -1), (8, 8), (-100, -100), (100, 100),
        
        # Invalid types
        (3.5, 4), (4, 3.5),  # Floats
        ("a", 4), (4, "b")   # Strings
    ]
    
    for pos in invalid_positions:
        try:
            moves = white_king.get_valid_moves(pos, board)
            assert moves == [], f"Invalid position {pos} should return empty list, got {moves}"
        except (TypeError, ValueError) as e:
            # It's also acceptable for the method to raise an exception for invalid types
            assert isinstance(pos[0], (str, float)) or isinstance(pos[1], (str, float)), \
                f"Unexpected exception for position {pos}: {str(e)}"

def test_king_kingside_castling(white_king, board):
    """Test kingside castling is allowed when all conditions are met"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[7][4] = white_king
    board.board[7][7] = Rook(Color.WHITE)
    white_king.has_moved = False
    Rook(Color.WHITE).has_moved = False
    board.current_turn = Color.WHITE
    board.en_passant_target = None
    # No pieces between king and rook, not in check
    valid_moves = white_king.get_valid_moves((7, 4), board)
    assert (7, 6) in valid_moves, "Kingside castling should be allowed"

def test_king_queenside_castling(white_king, board):
    """Test queenside castling is allowed when all conditions are met"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[7][4] = white_king
    board.board[7][0] = Rook(Color.WHITE)
    white_king.has_moved = False
    Rook(Color.WHITE).has_moved = False
    board.current_turn = Color.WHITE
    board.en_passant_target = None
    # No pieces between king and rook, not in check
    valid_moves = white_king.get_valid_moves((7, 4), board)
    assert (7, 2) in valid_moves, "Queenside castling should be allowed"

def test_king_castling_blocked(white_king, board):
    """Test castling is not allowed if path is blocked"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[7][4] = white_king
    board.board[7][7] = Rook(Color.WHITE)
    board.board[7][5] = Rook(Color.WHITE)  # Block path
    white_king.has_moved = False
    Rook(Color.WHITE).has_moved = False
    board.current_turn = Color.WHITE
    board.en_passant_target = None
    valid_moves = white_king.get_valid_moves((7, 4), board)
    assert (7, 6) not in valid_moves, "Kingside castling should not be allowed"

def test_king_castling_king_moved(white_king, board):
    """Test castling is not allowed if king has moved"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[7][4] = white_king
    board.board[7][7] = Rook(Color.WHITE)
    white_king.has_moved = True
    Rook(Color.WHITE).has_moved = False
    board.current_turn = Color.WHITE
    board.en_passant_target = None
    valid_moves = white_king.get_valid_moves((7, 4), board)
    assert (7, 6) not in valid_moves, "Kingside castling should not be allowed"

def test_king_castling_rook_moved(white_king, board):
    """Test castling is not allowed if rook has moved"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[7][4] = white_king
    kingside_rook = Rook(Color.WHITE)
    board.board[7][7] = kingside_rook
    white_king.has_moved = False
    kingside_rook.has_moved = True  # Set has_moved on the actual rook instance
    board.current_turn = Color.WHITE
    board.en_passant_target = None
    valid_moves = white_king.get_valid_moves((7, 4), board)
    assert (7, 6) not in valid_moves, "Kingside castling should not be allowed" 