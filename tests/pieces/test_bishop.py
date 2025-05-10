import pytest
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.base import Color
from src.chess.board import Board

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def white_bishop():
    return Bishop(Color.WHITE)

@pytest.fixture
def black_bishop():
    return Bishop(Color.BLACK)

def test_symbols(white_bishop, black_bishop):
    """Test bishop symbols"""
    assert white_bishop.get_symbol() == '♗'
    assert black_bishop.get_symbol() == '♝'
    assert white_bishop.get_ascii_symbol() == 'B'
    assert black_bishop.get_ascii_symbol() == 'b'

def test_initial_moves(white_bishop, board):
    """Test bishop moves from starting position"""
    # Place white bishop at c1
    board.board[7][2] = white_bishop
    moves = white_bishop.get_valid_moves((7, 2), board)
    
    # Should have no moves initially due to pawns
    assert len(moves) == 0

def test_diagonal_moves(white_bishop, board):
    """Test bishop diagonal movement"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white bishop at d4
    board.board[4][3] = white_bishop
    
    moves = set(white_bishop.get_valid_moves((4, 3), board))
    expected_moves = {
        (3, 2), (2, 1), (1, 0),  # Northwest
        (3, 4), (2, 5), (1, 6), (0, 7),  # Northeast
        (5, 2), (6, 1), (7, 0),  # Southwest
        (5, 4), (6, 5), (7, 6)   # Southeast
    }
    
    assert moves == expected_moves, f"\nMissing moves: {expected_moves - moves}\nUnexpected moves: {moves - expected_moves}"

def test_capture_moves(white_bishop, black_bishop, board):
    """Test bishop capture moves"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white bishop at d4
    board.board[4][3] = white_bishop
    
    # Place black bishops in capture positions
    board.board[2][1] = black_bishop  # Northwest
    board.board[2][5] = black_bishop  # Northeast
    board.board[6][1] = black_bishop  # Southwest
    board.board[6][5] = black_bishop  # Southeast
    
    moves = set(white_bishop.get_valid_moves((4, 3), board))
    capture_moves = {(2, 1), (2, 5), (6, 1), (6, 5)}
    
    # Should be able to capture all black bishops
    assert capture_moves.issubset(moves), f"Missing capture moves: {capture_moves - moves}"

def test_blocked_moves(white_bishop, board):
    """Test bishop moves when blocked by pieces"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white bishop at d4
    board.board[4][3] = white_bishop
    
    # Place white bishops blocking the bishop
    board.board[3][2] = Bishop(Color.WHITE)  # Northwest
    board.board[3][4] = Bishop(Color.WHITE)  # Northeast
    board.board[5][2] = Bishop(Color.WHITE)  # Southwest
    board.board[5][4] = Bishop(Color.WHITE)  # Southeast
    
    moves = white_bishop.get_valid_moves((4, 3), board)
    
    # Should have no moves when blocked by own pieces
    assert len(moves) == 0

def test_edge_positions(white_bishop, board):
    """Test bishop moves from corner position"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place white bishop at corner
    board.board[0][0] = white_bishop
    
    moves = set(white_bishop.get_valid_moves((0, 0), board))
    expected_moves = {
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)
    }
    
    assert moves == expected_moves, f"\nMissing moves: {expected_moves - moves}\nUnexpected moves: {moves - expected_moves}"

def test_all_edge_positions(white_bishop, board):
    """Test bishop moves from various edge positions"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Test positions: middle of each edge (top, bottom, left, right)
    edge_test_cases = {
        # Top edge (0,3) - can move SE and SW
        (0,3): {(1,2), (2,1), (3,0),      # Southwest
                (1,4), (2,5), (3,6), (4,7)}, # Southeast
        
        # Bottom edge (7,3) - can move NE and NW
        (7,3): {(6,2), (5,1), (4,0),      # Northwest
                (6,4), (5,5), (4,6), (3,7)}, # Northeast
        
        # Left edge (3,0) - can move NE and SE
        (3,0): {(2,1), (1,2), (0,3),      # Northeast
                (4,1), (5,2), (6,3), (7,4)}, # Southeast
        
        # Right edge (3,7) - can move NW and SW
        (3,7): {(2,6), (1,5), (0,4),      # Northwest
                (4,6), (5,5), (6,4), (7,3)}  # Southwest
    }
    
    for pos, expected in edge_test_cases.items():
        # Reset board for each test
        board.board = [[None for _ in range(8)] for _ in range(8)]
        board.board[pos[0]][pos[1]] = white_bishop
        
        moves = set(white_bishop.get_valid_moves(pos, board))
        assert moves == expected, f"\nTesting position {pos}:\nMissing moves: {expected - moves}\nUnexpected moves: {moves - expected}"

def test_invalid_positions(white_bishop, board):
    """Test that invalid positions return empty move list"""
    # Create an empty board
    board.board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place a bishop on the board to ensure it's not affecting invalid position checks
    board.board[4][3] = white_bishop
    
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
            moves = white_bishop.get_valid_moves(pos, board)
            assert moves == [], f"Invalid position {pos} should return empty list, got {moves}"
        except (TypeError, ValueError) as e:
            # It's also acceptable for the method to raise an exception for invalid types
            assert isinstance(pos[0], (str, float)) or isinstance(pos[1], (str, float)), \
                f"Unexpected exception for position {pos}: {str(e)}"

def test_bishop_surrounded_by_friendly(white_bishop, board):
    """Test bishop has no moves when surrounded by friendly pieces"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[3][3] = white_bishop
    # Surround with white pieces
    for pos in [(2,2), (2,4), (4,2), (4,4)]:
        board.board[pos[0]][pos[1]] = Bishop(Color.WHITE)
    valid_moves = white_bishop.get_valid_moves((3,3), board)
    assert valid_moves == []

def test_black_bishop_moves(black_bishop, board):
    """Test black bishop moves"""
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[4][4] = black_bishop
    valid_moves = black_bishop.get_valid_moves((4,4), board)
    expected_moves = []
    # Diagonals
    for i in range(1, 4+1):
        if 4-i >= 0 and 4-i >= 0:
            expected_moves.append((4-i, 4-i))
        if 4-i >= 0 and 4+i < 8:
            expected_moves.append((4-i, 4+i))
        if 4+i < 8 and 4-i >= 0:
            expected_moves.append((4+i, 4-i))
        if 4+i < 8 and 4+i < 8:
            expected_moves.append((4+i, 4+i))
    for move in expected_moves:
        assert move in valid_moves 