import pytest
from chess.board import Board
from chess.engines import ChessEngine

def test_chess_engine_initialization():
    """Test that the base chess engine initializes correctly."""
    # This should raise TypeError since ChessEngine is abstract
    with pytest.raises(TypeError):
        engine = ChessEngine()

def test_chess_engine_abstract_methods():
    """Test that the base chess engine has the required abstract methods."""
    assert hasattr(ChessEngine, 'get_best_move')
    assert hasattr(ChessEngine, 'evaluate_position')
    
    # Check that the methods are abstract
    assert ChessEngine.get_best_move.__isabstractmethod__
    assert ChessEngine.evaluate_position.__isabstractmethod__ 