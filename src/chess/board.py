from typing import List, Tuple, Optional, Dict
from .pieces.base import Color, PieceType, Piece
from .pieces.pawn import Pawn
from .pieces.knight import Knight
from .pieces.bishop import Bishop
from .pieces.rook import Rook
from .pieces.queen import Queen
from .pieces.king import King

class Board:
    """A class representing a chess board and its state.
    
    This class manages the chess board state, including piece positions,
    move history, and game rules enforcement. It handles special moves like
    castling, en passant, and pawn promotion.
    """
    
    def __init__(self):
        """Initialize a new chess board with pieces in their starting positions.
        
        The board is initialized with:
        - An 8x8 grid of pieces
        - White's turn to move
        - Empty move history
        - No en passant target
        - Empty position history for threefold repetition
        - Fifty-move counter set to 0
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.move_history = []
        self.en_passant_target = None
        self.position_history = []  # For threefold repetition
        self.fifty_move_counter = 0  # For fifty-move rule
        self._initialize_board()
        self.position_history.append(self.get_board_state())

    def _initialize_board(self):
        """Initialize the board with pieces in their standard starting positions.
        
        Sets up:
        - Pawns on ranks 2 and 7
        - Other pieces on ranks 1 and 8 in standard order
        """
        # Set up pawns
        for col in range(8):
            self.board[1][col] = Pawn(Color.BLACK)
            self.board[6][col] = Pawn(Color.WHITE)

        # Set up other pieces
        piece_order = [
            (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)
        ]

        for col, piece_class in enumerate(piece_order[0]):
            self.board[0][col] = piece_class(Color.BLACK)
            self.board[7][col] = piece_class(Color.WHITE)

    def get_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        """Get the piece at the given position.
        
        Args:
            position: A tuple of (row, col) coordinates
            
        Returns:
            The piece at the given position, or None if the position is empty
            or out of bounds
        """
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def is_valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """Check if a move is valid according to chess rules.
        
        Args:
            start_pos: The starting position (row, col)
            end_pos: The ending position (row, col)
            
        Returns:
            True if the move is valid, False otherwise
            
        Note:
            A move is valid if:
            - Both positions are within bounds
            - There is a piece of the current player's color at start_pos
            - The piece can legally move to end_pos
            - The move doesn't leave the king in check
        """
        # Check if positions are within bounds
        if not (0 <= start_pos[0] < 8 and 0 <= start_pos[1] < 8 and 
                0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8):
            return False

        piece = self.get_piece(start_pos)
        if piece is None or piece.color != self.current_turn:
            return False

        if not piece.is_valid_move(start_pos, end_pos, self):
            return False

        # Try the move
        original_piece = self.get_piece(end_pos)
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None

        # Check if the move leaves the king in check
        in_check = self.is_check(self.current_turn)

        # Undo the move
        self.board[start_pos[0]][start_pos[1]] = piece
        self.board[end_pos[0]][end_pos[1]] = original_piece

        return not in_check

    def make_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], promotion_piece: Optional[PieceType] = None) -> bool:
        """Make a move on the board if it's valid.
        
        Args:
            start_pos: The starting position (row, col)
            end_pos: The ending position (row, col)
            promotion_piece: The piece type to promote to if it's a pawn promotion
                           (default: None, which promotes to queen)
            
        Returns:
            True if the move was made successfully, False otherwise
            
        Note:
            This method handles:
            - Regular moves
            - Castling
            - En passant captures
            - Pawn promotion
            - Updating move history and position history
            - Updating the fifty-move counter
        """
        if not self.is_valid_move(start_pos, end_pos):
            return False

        piece = self.board[start_pos[0]][start_pos[1]]

        # Check castling conditions
        if isinstance(piece, King) and abs(end_pos[1] - start_pos[1]) == 2:
            # Check if king is in check
            if self.is_check(piece.color):
                return False
            
            # Check if squares between king and rook are under attack
            row = start_pos[0]
            if end_pos[1] > start_pos[1]:  # Kingside
                if any(self.is_square_attacked((row, c), piece.color) for c in range(start_pos[1], end_pos[1] + 1)):
                    return False
            else:  # Queenside
                if any(self.is_square_attacked((row, c), piece.color) for c in range(end_pos[1], start_pos[1] + 1)):
                    return False

        # Store the move
        self.move_history.append((start_pos, end_pos, self.get_piece(end_pos)))

        # Update fifty-move counter
        captured_piece = self.get_piece(end_pos)
        if isinstance(piece, Pawn) or captured_piece is not None:
            self.fifty_move_counter = 0
        else:
            self.fifty_move_counter += 1

        # Make the move
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None
        piece.has_moved = True

        # Handle en passant capture
        if isinstance(piece, Pawn) and end_pos == self.en_passant_target:
            # Remove the captured pawn
            capture_row = start_pos[0]
            capture_col = end_pos[1]
            self.board[capture_row][capture_col] = None
            self.fifty_move_counter = 0  # Reset counter for capture

        # Handle pawn promotion
        if isinstance(piece, Pawn) and (end_pos[0] == 0 or end_pos[0] == 7):
            if promotion_piece is None:
                promotion_piece = PieceType.QUEEN
            if promotion_piece == PieceType.QUEEN:
                self.board[end_pos[0]][end_pos[1]] = Queen(piece.color)
            elif promotion_piece == PieceType.ROOK:
                self.board[end_pos[0]][end_pos[1]] = Rook(piece.color)
            elif promotion_piece == PieceType.BISHOP:
                self.board[end_pos[0]][end_pos[1]] = Bishop(piece.color)
            elif promotion_piece == PieceType.KNIGHT:
                self.board[end_pos[0]][end_pos[1]] = Knight(piece.color)

        # Update en passant target
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(end_pos[0] - start_pos[0]) == 2:
            self.en_passant_target = ((start_pos[0] + end_pos[0]) // 2, start_pos[1])

        # Handle castling
        if isinstance(piece, King) and abs(end_pos[1] - start_pos[1]) == 2:
            if end_pos[1] > start_pos[1]:  # Kingside
                rook = self.board[start_pos[0]][7]
                self.board[start_pos[0]][5] = rook
                self.board[start_pos[0]][7] = None
                rook.has_moved = True
            else:  # Queenside
                rook = self.board[start_pos[0]][0]
                self.board[start_pos[0]][3] = rook
                self.board[start_pos[0]][0] = None
                rook.has_moved = True

        # Update position history for threefold repetition
        self.position_history.append(self.get_board_state())

        # Switch turns
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True

    def undo_move(self) -> bool:
        """Undo the last move made on the board.
        
        Returns:
            True if a move was undone, False if there are no moves to undo
            
        Note:
            This method handles:
            - Restoring piece positions
            - Restoring captured pieces
            - Updating piece movement status
            - Restoring castling rights
            - Updating position history
            - Updating the fifty-move counter
            - Restoring the previous turn
        """
        if not self.move_history:
            return False

        start_pos, end_pos, captured_piece = self.move_history.pop()
        piece = self.board[end_pos[0]][end_pos[1]]
        
        # Restore the piece to its original position
        self.board[start_pos[0]][start_pos[1]] = piece
        self.board[end_pos[0]][end_pos[1]] = captured_piece
        piece.has_moved = False

        # Handle undoing castling
        if isinstance(piece, King) and abs(end_pos[1] - start_pos[1]) == 2:
            # Kingside castling
            if end_pos[1] > start_pos[1]:
                rook = self.board[start_pos[0]][5]
                self.board[start_pos[0]][7] = rook
                self.board[start_pos[0]][5] = None
                rook.has_moved = False
            # Queenside castling
            else:
                rook = self.board[start_pos[0]][3]
                self.board[start_pos[0]][0] = rook
                self.board[start_pos[0]][3] = None
                rook.has_moved = False

        # Remove the last position from history
        if self.position_history:
            self.position_history.pop()

        # Restore fifty move counter (decrement by 1 or reset if it was reset)
        if isinstance(piece, Pawn) or captured_piece is not None:
            self.fifty_move_counter = 0
        else:
            self.fifty_move_counter = max(0, self.fifty_move_counter - 1)

        # Switch turns back
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True

    def is_check(self, color: Color) -> bool:
        """Check if the given color's king is in check.
        
        Args:
            color: The color of the king to check
            
        Returns:
            True if the king is in check, False otherwise
            
        Note:
            Checks for attacks from:
            - Pawns
            - Knights
            - Bishops and Queens (diagonal)
            - Rooks and Queens (straight)
            - Kings (adjacent squares)
        """
        # Find the king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        # Check if any opponent piece can capture the king
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        king_row, king_col = king_pos

        # Check for pawn attacks
        pawn_direction = 1 if color == Color.WHITE else -1
        for dcol in [-1, 1]:
            attack_row = king_row + pawn_direction
            attack_col = king_col + dcol
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                piece = self.board[attack_row][attack_col]
                if isinstance(piece, Pawn) and piece.color == opponent_color:
                    return True

        # Check for knight attacks
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for drow, dcol in knight_moves:
            attack_row = king_row + drow
            attack_col = king_col + dcol
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                piece = self.board[attack_row][attack_col]
                if isinstance(piece, Knight) and piece.color == opponent_color:
                    return True

        # Check for diagonal attacks (bishop/queen)
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for drow, dcol in diagonals:
            current_row = king_row + drow
            current_col = king_col + dcol
            while 0 <= current_row < 8 and 0 <= current_col < 8:
                piece = self.board[current_row][current_col]
                if piece:
                    if piece.color == opponent_color and (
                        isinstance(piece, Bishop) or 
                        isinstance(piece, Queen)
                    ):
                        return True
                    break
                current_row += drow
                current_col += dcol

        # Check for straight attacks (rook/queen)
        straights = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for drow, dcol in straights:
            current_row = king_row + drow
            current_col = king_col + dcol
            while 0 <= current_row < 8 and 0 <= current_col < 8:
                piece = self.board[current_row][current_col]
                if piece:
                    if piece.color == opponent_color and (
                        isinstance(piece, Rook) or 
                        isinstance(piece, Queen)
                    ):
                        return True
                    break
                current_row += drow
                current_col += dcol

        # Check for king attacks (for adjacent kings)
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for drow, dcol in king_moves:
            attack_row = king_row + drow
            attack_col = king_col + dcol
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                piece = self.board[attack_row][attack_col]
                if isinstance(piece, King) and piece.color == opponent_color:
                    return True

        return False

    def is_checkmate(self, color: Color) -> bool:
        """Check if the given color is in checkmate.
        
        Args:
            color: The color to check for checkmate
            
        Returns:
            True if the color is in checkmate, False otherwise
            
        Note:
            A position is checkmate if:
            - The king is in check
            - No legal moves are available to get out of check
        """
        if not self.is_check(color):
            return False

        # Try all possible moves for all pieces of the given color
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.get_valid_moves((row, col), self):
                        # Try the move
                        original_piece = self.board[move[0]][move[1]]
                        self.board[move[0]][move[1]] = piece
                        self.board[row][col] = None

                        # Check if still in check
                        still_in_check = self.is_check(color)

                        # Undo the move
                        self.board[row][col] = piece
                        self.board[move[0]][move[1]] = original_piece

                        if not still_in_check:
                            return False
        return True

    def is_stalemate(self) -> bool:
        """Check if the current position is a stalemate.
        
        Returns:
            True if the position is a stalemate, False otherwise
            
        Note:
            A position is stalemate if:
            - The current player is not in check
            - The current player has no legal moves
        """
        if self.is_check(self.current_turn):
            return False

        # Check if any legal moves exist
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_turn:
                    for move in piece.get_valid_moves((row, col), self):
                        # Only count moves that are actually legal (do not leave king in check)
                        if self.is_valid_move((row, col), move):
                            return False
        return True

    def get_board_state(self) -> str:
        """Get the current board state in FEN-like format.
        
        Returns:
            A string representing the board state in a format similar to FEN,
            including:
            - Piece positions
            - Current turn
            - Castling rights
            - En passant target square
            
        Note:
            This format is used for detecting threefold repetition.
        """
        # Get piece positions
        state = []
        for row in range(8):
            empty_count = 0
            row_str = ""
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    row_str += piece.get_ascii_symbol()
            if empty_count > 0:
                row_str += str(empty_count)
            state.append(row_str)
        position = "/".join(state)

        # Add turn
        position += " w " if self.current_turn == Color.WHITE else " b "

        # Add castling rights
        castling = ""
        # White kingside
        if (self.get_piece((7, 4)) and 
            isinstance(self.get_piece((7, 4)), King) and 
            not self.get_piece((7, 4)).has_moved and
            self.get_piece((7, 7)) and 
            isinstance(self.get_piece((7, 7)), Rook) and 
            not self.get_piece((7, 7)).has_moved):
            castling += "K"
        # White queenside
        if (self.get_piece((7, 4)) and 
            isinstance(self.get_piece((7, 4)), King) and 
            not self.get_piece((7, 4)).has_moved and
            self.get_piece((7, 0)) and 
            isinstance(self.get_piece((7, 0)), Rook) and 
            not self.get_piece((7, 0)).has_moved):
            castling += "Q"
        # Black kingside
        if (self.get_piece((0, 4)) and 
            isinstance(self.get_piece((0, 4)), King) and 
            not self.get_piece((0, 4)).has_moved and
            self.get_piece((0, 7)) and 
            isinstance(self.get_piece((0, 7)), Rook) and 
            not self.get_piece((0, 7)).has_moved):
            castling += "k"
        # Black queenside
        if (self.get_piece((0, 4)) and 
            isinstance(self.get_piece((0, 4)), King) and 
            not self.get_piece((0, 4)).has_moved and
            self.get_piece((0, 0)) and 
            isinstance(self.get_piece((0, 0)), Rook) and 
            not self.get_piece((0, 0)).has_moved):
            castling += "q"
        position += castling if castling else "-"

        # Add en passant target
        if self.en_passant_target:
            file = chr(self.en_passant_target[1] + ord('a'))
            rank = str(8 - self.en_passant_target[0])
            position += f" {file}{rank}"
        else:
            position += " -"

        return position

    def is_square_attacked(self, square: Tuple[int, int], color: Color) -> bool:
        """Check if a square is under attack by the opponent.
        
        Args:
            square: The square to check (row, col)
            color: The color of the player whose pieces are being checked for attacks
            
        Returns:
            True if the square is under attack, False otherwise
            
        Note:
            This method is used to check if castling is legal by verifying
            that the squares between the king and rook are not under attack.
        """
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    if square in piece.get_valid_moves((row, col), self):
                        return True
        return False

    def is_threefold_repetition(self) -> bool:
        """Check if the current position has occurred three times.
        
        Returns:
            True if the current position has occurred three or more times,
            False otherwise
            
        Note:
            This is used to detect draws by threefold repetition.
            The position history includes piece positions, turn, castling rights,
            and en passant target square.
        """
        current_position = self.get_board_state()
        return self.position_history.count(current_position) >= 3

    def is_fifty_moves(self) -> bool:
        """Check if fifty moves have been made without a pawn move or capture.
        
        Returns:
            True if fifty moves have been made without a pawn move or capture,
            False otherwise
            
        Note:
            This is used to detect draws by the fifty-move rule.
            The counter is reset when a pawn moves or a piece is captured.
        """
        return self.fifty_move_counter >= 50

    def is_insufficient_material(self) -> bool:
        """Check if there is insufficient material to checkmate.
        
        Returns:
            True if there is insufficient material to checkmate,
            False otherwise
            
        Note:
            Insufficient material occurs when:
            - Only kings remain
            - King and knight vs king
            - King and bishop vs king
            - King and bishop vs king and bishop (same color squares)
        """
        pieces = {Color.WHITE: [], Color.BLACK: []}
        
        # Count pieces for each color
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None:
                    pieces[piece.color].append(type(piece))

        # Check for insufficient material patterns
        for color in Color:
            opponent = Color.BLACK if color == Color.WHITE else Color.WHITE
            if len(pieces[color]) == 1:  # Only king
                return True
            if len(pieces[color]) == 2:
                if Knight in pieces[color] or Bishop in pieces[color]:
                    return True
            if len(pieces[color]) == 2 and len(pieces[opponent]) == 1:
                if Knight in pieces[color] or Bishop in pieces[color]:
                    return True

        return False 