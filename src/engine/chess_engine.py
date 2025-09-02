from .board_manager import BoardManager
from .game_state import GameState
from .move_validator import MoveValidator
from .rules_engine import RulesEngine


class ChessEngine:
    """Main chess engine that coordinates all game components"""

    def __init__(self, board=None):
        """Initialize chess engine with all modular components"""
        # Initialize core components
        self.board_manager = BoardManager(board)
        self.game_state = GameState()
        self.move_validator = MoveValidator(self.board_manager)
        self.rules_engine = RulesEngine(self.board_manager, self.move_validator)

        # # Initialize AI components
        # self.ai = ChessAI(self)
        # self.position_evaluator = PositionEvaluator(self.board_manager)

    def select_piece(self, row, col):
        """Select a piece at the given position if it belongs to current player"""
        piece = self.board_manager.get_piece(row, col)

        if (
            piece
            and piece[0] == self.game_state.get_current_player()
            and self.board_manager.is_position_valid(row, col)
        ):
            # Remove piece from board and select it
            self.board_manager.remove_piece(row, col)
            self.game_state.select_piece(piece, (row, col))
            return True
        return False

    def make_move(self, to_row, to_col):
        """Attempt to move selected piece to destination"""
        if not self.game_state.has_selected_piece():
            return False

        piece = self.game_state.get_selected_piece()
        from_pos = self.game_state.get_selected_position()

        if self.move_validator.is_valid_move(piece, from_pos, (to_row, to_col)):
            # Capture any piece at destination
            captured_piece = self.board_manager.get_piece(to_row, to_col)

            # Make the move
            self.board_manager.set_piece(to_row, to_col, piece)

            # Update game state
            self.game_state.add_move(from_pos, (to_row, to_col), piece, captured_piece)
            self.game_state.switch_player()
            self.game_state.clear_selection()

            return True
        else:
            self._return_piece()
            return False

    def cancel_selection(self):
        """Cancel current piece selection"""
        self._return_piece()

    def _return_piece(self):
        """Return selected piece to original position"""
        if self.game_state.has_selected_piece():
            piece = self.game_state.get_selected_piece()
            pos = self.game_state.get_selected_position()

            if pos:
                self.board_manager.set_piece(pos[0], pos[1], piece)

            self.game_state.clear_selection()

    def reset_game(self):
        """Reset the game to initial state"""
        self.board_manager.reset_board()
        self.game_state.reset_game()
