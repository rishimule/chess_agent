import pytest
from src.chess.board import Board
from src.chess.pieces.base import Color, PieceType
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.rook import Rook
from src.chess.pieces.knight import Knight
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.queen import Queen
from src.chess.pieces.king import King

@pytest.fixture
def board():
    return Board()

def test_board_initialization(board):
    # Check pawns
    for col in range(8):
        assert isinstance(board.board[1][col], Pawn)
        assert board.board[1][col].color == Color.BLACK
        assert isinstance(board.board[6][col], Pawn)
        assert board.board[6][col].color == Color.WHITE
    # Check major pieces
    assert isinstance(board.board[0][0], Rook)
    assert isinstance(board.board[0][1], Knight)
    assert isinstance(board.board[0][2], Bishop)
    assert isinstance(board.board[0][3], Queen)
    assert isinstance(board.board[0][4], King)
    assert isinstance(board.board[0][5], Bishop)
    assert isinstance(board.board[0][6], Knight)
    assert isinstance(board.board[0][7], Rook)
    assert isinstance(board.board[7][0], Rook)
    assert isinstance(board.board[7][1], Knight)
    assert isinstance(board.board[7][2], Bishop)
    assert isinstance(board.board[7][3], Queen)
    assert isinstance(board.board[7][4], King)
    assert isinstance(board.board[7][5], Bishop)
    assert isinstance(board.board[7][6], Knight)
    assert isinstance(board.board[7][7], Rook)
    # Check empty squares
    for row in range(2, 6):
        for col in range(8):
            assert board.board[row][col] is None

def test_get_piece(board):
    assert isinstance(board.get_piece((0, 0)), Rook)
    assert board.get_piece((4, 4)) is None
    assert board.get_piece((-1, 0)) is None
    assert board.get_piece((8, 8)) is None

def test_is_valid_move_and_make_move(board):
    # Move white pawn e2 to e4
    assert board.is_valid_move((6, 4), (4, 4))
    assert board.make_move((6, 4), (4, 4))
    # Now it's black's turn, move pawn e7 to e5
    assert board.is_valid_move((1, 4), (3, 4))
    assert board.make_move((1, 4), (3, 4))
    # Invalid move: white tries to move black's pawn
    assert not board.is_valid_move((3, 4), (4, 4))
    # Invalid move: move to same square
    assert not board.is_valid_move((4, 4), (4, 4))

def test_undo_move(board):
    board.make_move((6, 4), (4, 4))  # e2-e4
    board.make_move((1, 4), (3, 4))  # e7-e5
    assert board.undo_move()  # Undo e7-e5
    assert board.board[1][4] is not None
    assert board.board[3][4] is None
    assert board.undo_move()  # Undo e2-e4
    assert board.board[6][4] is not None
    assert board.board[4][4] is None
    # Nothing to undo
    assert not board.undo_move()

def test_check_detection():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[0][4] = King(Color.BLACK)
    b.board[7][4] = King(Color.WHITE)
    b.board[1][4] = Queen(Color.WHITE)  # White queen gives check
    assert b.is_check(Color.BLACK)
    assert not b.is_check(Color.WHITE)

def test_checkmate_detection():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[0][4] = King(Color.BLACK)
    b.board[7][4] = King(Color.WHITE)
    b.board[1][4] = Queen(Color.WHITE)
    b.board[1][5] = Rook(Color.WHITE)
    assert b.is_checkmate(Color.BLACK)
    assert not b.is_checkmate(Color.WHITE)

def test_stalemate_detection():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[0][7] = King(Color.BLACK)
    b.board[2][6] = Queen(Color.WHITE)
    b.board[1][5] = King(Color.WHITE)
    b.current_turn = Color.BLACK
    assert b.is_stalemate()

def test_castling(board):
    # Set up empty board for castling
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.board[7][4] = King(Color.WHITE)
    kingside_rook = Rook(Color.WHITE)
    queenside_rook = Rook(Color.WHITE)
    board.board[7][7] = kingside_rook
    board.board[7][0] = queenside_rook
    board.current_turn = Color.WHITE
    # Kingside castling
    assert board.is_valid_move((7, 4), (7, 6))
    assert board.make_move((7, 4), (7, 6))
    # Undo and try queenside
    board.undo_move()
    assert board.is_valid_move((7, 4), (7, 2))
    assert board.make_move((7, 4), (7, 2))

def test_en_passant():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[3][4] = Pawn(Color.WHITE)
    b.board[1][5] = Pawn(Color.BLACK)
    b.current_turn = Color.BLACK
    b.make_move((1, 5), (3, 5))  # Black pawn moves two squares
    b.current_turn = Color.WHITE
    b.en_passant_target = (2, 5)
    assert b.is_valid_move((3, 4), (2, 5))
    assert b.make_move((3, 4), (2, 5))
    assert b.board[3][5] is None  # Captured pawn

def test_pawn_promotion():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[1][0] = Pawn(Color.WHITE)
    b.current_turn = Color.WHITE
    assert b.make_move((1, 0), (0, 0), promotion_piece=PieceType.QUEEN)
    assert isinstance(b.board[0][0], Queen)
    # Test default promotion to queen
    b.board[1][1] = Pawn(Color.WHITE)
    b.current_turn = Color.WHITE  # Ensure it's white's turn again
    assert b.make_move((1, 1), (0, 1))
    assert isinstance(b.board[0][1], Queen)

def test_get_board_state_and_history(board):
    state1 = board.get_board_state()
    board.make_move((6, 4), (4, 4))
    # The state stored in position_history is with the turn before the switch
    state2 = board.position_history[-1]
    assert state1 != state2
    # Test position history
    assert state1 in board.position_history
    assert state2 in board.position_history

def test_threefold_repetition():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[0][4] = King(Color.BLACK)
    b.board[7][4] = King(Color.WHITE)
    b.board[1][0] = Rook(Color.WHITE)
    b.board[6][7] = Rook(Color.BLACK)
    b.current_turn = Color.WHITE
    # Set has_moved to True to remove castling rights from FEN
    b.board[0][4].has_moved = True
    b.board[7][4].has_moved = True
    b.board[1][0].has_moved = True
    b.board[6][7].has_moved = True
    b.en_passant_target = None
    for _ in range(3):
        b.make_move((1, 0), (0, 0))  # White rook up
        b.position_history.append(b.get_board_state())
        b.make_move((6, 7), (7, 7))  # Black rook down
        b.position_history.append(b.get_board_state())
        b.make_move((0, 0), (1, 0))  # White rook back
        b.position_history.append(b.get_board_state())
        b.make_move((7, 7), (6, 7))  # Black rook back
        b.position_history.append(b.get_board_state())
    repeated_fen = b.get_board_state()
    assert b.position_history.count(repeated_fen) >= 3
    assert b.is_threefold_repetition()

def test_fifty_move_rule():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[0][4] = King(Color.BLACK)
    b.board[7][4] = King(Color.WHITE)
    b.fifty_move_counter = 50
    assert b.is_fifty_moves()

def test_insufficient_material():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.board[0][4] = King(Color.BLACK)
    b.board[7][4] = King(Color.WHITE)
    assert b.is_insufficient_material()
    # King and bishop vs king
    b.board[3][3] = Bishop(Color.WHITE)
    assert b.is_insufficient_material()
    # King and knight vs king
    b.board[3][3] = Knight(Color.WHITE)
    assert b.is_insufficient_material()
    # King and bishop vs king and bishop
    b.board[3][3] = Bishop(Color.WHITE)
    b.board[4][4] = Bishop(Color.BLACK)
    assert b.is_insufficient_material() 