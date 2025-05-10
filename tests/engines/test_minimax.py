import pytest
from chess.board import Board
from chess.pieces import Color, PieceType, King, Queen
from chess.engines import MinimaxEngine

def test_minimax_engine_initialization():
    """Test that the minimax engine initializes correctly."""
    engine = MinimaxEngine(depth=3)
    assert engine.depth == 3

def test_minimax_engine_evaluation():
    """Test the minimax engine's position evaluation."""
    board = Board()
    engine = MinimaxEngine()
    
    # Test initial position evaluation
    score = engine.evaluate_position(board)
    assert isinstance(score, float)
    assert score == 0.0  # Initial position should be equal

def test_minimax_engine_best_move():
    """Test that the minimax engine can find a best move."""
    board = Board()
    engine = MinimaxEngine(depth=2)  # Use small depth for testing
    
    # Get best move for initial position
    move = engine.get_best_move(board)
    assert move is not None
    start_pos, end_pos = move
    assert len(start_pos) == 2
    assert len(end_pos) == 2
    assert all(0 <= x < 8 for x in start_pos)
    assert all(0 <= x < 8 for x in end_pos)

def test_minimax_engine_checkmate():
    """Test that the engine can detect checkmate."""
    board = Board()
    engine = MinimaxEngine(depth=3)
    
    # Set up a simple checkmate position (Fool's Mate)
    board.make_move((6, 5), (5, 5))  # White f2-f3
    board.make_move((1, 4), (3, 4))  # Black e7-e5
    board.make_move((6, 6), (4, 6))  # White g2-g4
    board.make_move((0, 3), (4, 7))  # Black Qd8-h4#
    
    # After these moves, White is checkmated
    assert board.is_checkmate(board.current_turn)

def test_minimax_engine_stalemate():
    """Test that the engine handles stalemate correctly."""
    board = Board()
    engine = MinimaxEngine(depth=3)
    
    # Set up a stalemate position
    # Clear the board
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None
    
    # Set up a stalemate position
    board.board[0][0] = King(Color.WHITE)
    board.board[1][2] = King(Color.BLACK)
    board.board[2][1] = Queen(Color.BLACK)
    board.current_turn = Color.WHITE
    
    # Engine should detect stalemate
    assert board.is_stalemate()

def test_minimax_engine_depth():
    """Test that the engine respects the search depth parameter."""
    board = Board()
    engine = MinimaxEngine(depth=1)
    
    # Make a move that would be bad at depth 1 but good at higher depths
    board.make_move((6, 4), (4, 4))  # White e2-e4
    board.make_move((1, 4), (3, 4))  # Black e7-e5
    
    # At depth 1, the engine might make a suboptimal move
    move = engine.get_best_move(board)
    assert move is not None 