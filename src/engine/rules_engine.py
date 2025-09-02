class RulesEngine:
    """Handles advanced chess rules like check, checkmate, castling, etc."""

    def __init__(self, board_manager, move_validator):
        """Initialize with references to board manager and move validator"""
        self.board_manager = board_manager
        self.move_validator = move_validator

    def is_in_check(self, player_color):
        """Check if the given player is in check"""
        # Find the king
        king_pos = self._find_king(player_color)
        if not king_pos:
            return False

        # Check if any opponent piece can attack the king
        opponent_color = "b" if player_color == "w" else "w"
        opponent_pieces = self.board_manager.get_pieces_for_player(opponent_color)

        for (row, col), piece in opponent_pieces:
            if self.move_validator.is_valid_move(piece, (row, col), king_pos):
                return True

        return False

    def is_checkmate(self, player_color):
        """Check if the given player is in checkmate"""
        # Must be in check first
        if not self.is_in_check(player_color):
            return False

        # Check if player has any legal moves that get out of check
        return not self._has_legal_moves_out_of_check(player_color)

    def is_stalemate(self, player_color):
        """Check if the given player is in stalemate"""
        # Must NOT be in check
        if self.is_in_check(player_color):
            return False

        # Check if player has no legal moves
        legal_moves = self.move_validator.get_all_legal_moves(player_color)
        return len(legal_moves) == 0

    def can_castle_kingside(self, player_color):
        """Check if kingside castling is legal"""
        # TODO: Implement castling rules
        # Need to check:
        # - King and rook haven't moved
        # - No pieces between king and rook
        # - King not in check
        # - King doesn't move through check
        return False

    def can_castle_queenside(self, player_color):
        """Check if queenside castling is legal"""
        # TODO: Implement castling rules
        return False

    def is_en_passant_valid(self, from_pos, to_pos, move_history):
        """Check if en passant capture is valid"""
        # TODO: Implement en passant rules
        # Need to check last move was a two-square pawn move
        return False

    def is_promotion_move(self, piece, to_pos):
        """Check if move results in pawn promotion"""
        if piece[1] != "P":  # Not a pawn
            return False

        to_row, to_col = to_pos

        # White pawn reaching rank 8 (row 0)
        if piece[0] == "w" and to_row == 0:
            return True

        # Black pawn reaching rank 1 (row 7)
        if piece[0] == "b" and to_row == 7:
            return True

        return False

    def _find_king(self, player_color):
        """Find the position of the king for given player"""
        king_piece = player_color + "K"

        for row in range(8):
            for col in range(8):
                if self.board_manager.get_piece(row, col) == king_piece:
                    return (row, col)
        return None

    def _has_legal_moves_out_of_check(self, player_color):
        """Check if player has any moves that get out of check"""
        # TODO: For each possible move, simulate it and check if still in check
        # This requires move simulation functionality

        # For now, return True (assume player can get out of check)
        # This prevents false checkmate detection
        return True

    def _simulate_move_and_check(self, from_pos, to_pos, player_color):
        """Simulate a move and check if player is still in check"""
        # TODO: Implement move simulation
        # 1. Make the move temporarily
        # 2. Check if player is in check
        # 3. Undo the move
        # 4. Return check status
        pass
