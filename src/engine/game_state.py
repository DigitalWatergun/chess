class GameState:
    """Manages game state including turns, selections, and move history"""

    def __init__(self):
        """Initialize game state"""
        self.current_player = "w"  # 'w' for white, 'b' for black
        self.selected_piece = ""
        self.selected_pos = (-1, -1)
        self.captured_piece = ""
        self.captured_pos = (-1, -1)
        self.move_history = []
        self.game_status = "active"  # 'active', 'check_b', 'check_w', 'checkmate', 'stalemate', 'draw', 'complete'
        self.white_castle = True
        self.black_castle = True
        self.pawn_promotion = False

    def switch_player(self):
        """Switch to the other player's turn"""
        self.current_player = "b" if self.current_player == "w" else "w"

    def set_current_player(self, player):
        """Set the current player ('w' or 'b')"""
        if player in ["w", "b"]:
            self.current_player = player

    def set_select_piece(self, piece, position):
        """Select a piece for movement"""
        self.selected_piece = piece
        self.selected_pos = position

    def set_capture_piece(self, piece, position):
        """Set a piece in the captured_piece and captured_pos if it exists"""
        self.captured_piece = piece
        self.captured_pos = position

    def clear_selection(self):
        """Clear current piece selection"""
        self.selected_piece = ""
        self.selected_pos = (-1, -1)

    def clear_captured(self):
        """Clear current captured piece"""
        self.captured_piece = ""
        self.captured_pos = (-1, -1)

    def add_move(self, from_pos, to_pos, piece, captured_piece=None):
        """Add a move to the history"""
        move = {
            "from": from_pos,
            "to": to_pos,
            "piece": piece,
            "captured": captured_piece,
            "player": self.current_player,
        }
        self.move_history.append(move)

    def get_move_history(self):
        """Get the complete move history"""
        return self.move_history.copy()

    def get_last_move(self):
        """Get the last move made"""
        return self.move_history[-1] if self.move_history else None

    def get_move_count(self):
        """Get the total number of moves made"""
        return len(self.move_history)

    def can_castle(self):
        if self.current_player == "w" and self.white_castle:
            return True
        elif self.current_player == "b" and self.black_castle:
            return True

        return False

    def set_castle(self):
        if self.current_player == "w":
            self.white_castle = False
        elif self.current_player == "b":
            self.black_castle = False

    def set_game_status(self, status):
        """Set the game status"""
        valid_statuses = ["active", "check", "checkmate", "stalemate", "draw"]
        if status in valid_statuses:
            self.game_status = status

    def get_game_status(self):
        """Get the current game status"""
        return self.game_status

    def is_game_over(self):
        """Check if the game is over"""
        return self.game_status in ["checkmate", "stalemate", "draw"]

    def reset_game(self):
        """Reset game state to initial conditions"""
        self.current_player = "w"
        self.selected_piece = ""
        self.selected_pos = (-1, -1)
        self.captured_piece = ""
        self.captured_pos = (-1, -1)
        self.move_history = []
        self.game_status = "active"
        self.white_castle = True
        self.black_castle = True
