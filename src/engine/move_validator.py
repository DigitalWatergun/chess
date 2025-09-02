from src.engine import valid_moves


class MoveValidator:
    """Handles all move validation logic"""

    def __init__(self, board_manager):
        """Initialize with reference to board manager"""
        self.board_manager = board_manager

    def is_valid_move(self, piece, from_pos, to_pos):
        """Check if a move is valid according to chess rules"""
        # Check within boundaries
        to_row, to_col = to_pos
        if not self.board_manager.is_position_valid(to_row, to_col):
            return False

        piece_type = piece[1]

        if piece_type == "P":
            return valid_moves.check_pawn_moves(
                self.board_manager.board, piece, from_pos, to_pos
            )
        elif piece_type == "R":
            return valid_moves.check_rook_moves(
                self.board_manager.board, piece, from_pos, to_pos
            )
        elif piece_type == "N":
            return valid_moves.check_knight_moves(from_pos, to_pos)
        elif piece_type == "B":
            return valid_moves.check_bishop_moves(from_pos, to_pos)
        elif piece_type == "Q":
            return valid_moves.check_queen_moves(from_pos, to_pos)
        elif piece_type == "K":
            return valid_moves.check_king_moves(from_pos, to_pos)

        return False

    def get_all_legal_moves(self, player_color):
        """Get all legal moves for a given player"""
        legal_moves = []
        pieces = self.board_manager.get_pieces_for_player(player_color)

        for (row, col), piece in pieces:
            piece_moves = self.get_legal_moves_for_piece(row, col)
            for move in piece_moves:
                legal_moves.append(((row, col), move, piece))

        return legal_moves

    def get_legal_moves_for_piece(self, row, col):
        """Get all legal moves for a piece at given position"""
        piece = self.board_manager.get_piece(row, col)
        if not piece:
            return []

        legal_moves = []

        # Check all possible destinations on the board
        for to_row in range(8):
            for to_col in range(8):
                if (to_row, to_col) != (row, col):  # Don't include current position
                    if self.is_valid_move(piece, (row, col), (to_row, to_col)):
                        legal_moves.append((to_row, to_col))

        return legal_moves

    def can_piece_move(self, row, col):
        """Check if a piece at given position has any legal moves"""
        return len(self.get_legal_moves_for_piece(row, col)) > 0

    def is_move_blocked(self, from_pos, to_pos):
        """Check if path between positions is blocked (for sliding pieces)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Calculate direction
        row_dir = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_dir = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        # Check each square in the path (excluding start and end)
        current_row, current_col = from_row + row_dir, from_col + col_dir

        while (current_row, current_col) != (to_row, to_col):
            if not self.board_manager.is_position_empty(current_row, current_col):
                return True
            current_row += row_dir
            current_col += col_dir

        return False

    def is_capture_move(self, piece, to_pos):
        """Check if move is a capture (destination has opponent piece)"""
        to_row, to_col = to_pos
        target_piece = self.board_manager.get_piece(to_row, to_col)

        if target_piece and target_piece[0] != piece[0]:  # Different colors
            return True
        return False
