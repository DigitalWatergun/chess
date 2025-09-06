class GameState:
    """Manages game state including turns, selections, and move history"""

    def __init__(self):
        """Initialize game state"""
        self.current_player = "w"  # 'w' for white, 'b' for black
        self.selected_piece = None
        self.selected_pos = None
        self.move_history = []
        self.game_status = (
            "active"  # 'active', 'check', 'checkmate', 'stalemate', 'draw'
        )

    def get_current_player(self):
        """Get the current player"""
        return self.current_player

    def switch_player(self):
        """Switch to the other player's turn"""
        self.current_player = "b" if self.current_player == "w" else "w"

    def set_current_player(self, player):
        """Set the current player ('w' or 'b')"""
        if player in ["w", "b"]:
            self.current_player = player

    def select_piece(self, piece, position):
        """Select a piece for movement"""
        self.selected_piece = piece
        self.selected_pos = position

    def clear_selection(self):
        """Clear current piece selection"""
        self.selected_piece = None
        self.selected_pos = None

    def has_selected_piece(self):
        """Check if a piece is currently selected"""
        return self.selected_piece is not None

    def get_selected_piece(self):
        """Get the currently selected piece"""
        return self.selected_piece

    def get_selected_position(self):
        """Get the position of the currently selected piece"""
        return self.selected_pos

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
        self.selected_piece = None
        self.selected_pos = None
        self.move_history = []
        self.game_status = "active"
