import os

import pygame

from config import COLORS, PIECE_COLORS, PIECE_TYPES, PIECES_DIR
from engine.board_manager import BoardManager
from engine.game_state import GameState
from engine.move_validator import MoveValidator
from engine.rules_engine import RulesEngine


class ChessEngine:
    """Main chess engine that coordinates all game components"""

    def __init__(self, board=None):
        """Initialize chess engine with all modular components"""
        # Initialize core components
        self.board_manager = BoardManager(board)
        self.game_state = GameState()
        self.move_validator = MoveValidator(self.board_manager, self.game_state)
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
        to_pos = (to_row, to_col)
        print(
            f"Selected_piece: {piece} -- Starting Pos: {from_pos} -- Ending Pos {to_pos}"
        )

        if self.move_validator.is_valid_move(to_pos):
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

    def init_pygame(self, width, height, title="Chess"):
        """Initialize pygame with error checking."""
        try:
            pygame.init()
            if not pygame.get_init():
                raise RuntimeError("Pygame failed to initialize")

            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
            return screen
        except pygame.error as e:
            raise RuntimeError(f"Failed to initialize pygame display: {e}")

    def load_piece_images(self, square_size):
        """Load and scale piece images, returning a dictionary of piece images."""
        piece_images = {}

        for c in PIECE_COLORS:
            for p in PIECE_TYPES:
                piece_code = c + p
                filename = f"{piece_code}.png"
                path = os.path.join(PIECES_DIR, filename)

                if not os.path.exists(path):
                    raise FileNotFoundError(f"Required piece image not found: {path}")

                try:
                    img = pygame.image.load(path)
                    img = pygame.transform.smoothscale(img, (square_size, square_size))
                    piece_images[piece_code] = img
                except pygame.error as e:
                    raise RuntimeError(f"Failed to load piece image {filename}: {e}")

        return piece_images

    def draw_board(self, screen, piece_images, square_size):
        """Draw the chess board with pieces."""
        board = self.board_manager.board
        square_colors = [COLORS["light_square"], COLORS["dark_square"]]

        for r in range(8):
            for c in range(8):
                color = square_colors[(r + c) % 2]
                rect = pygame.Rect(
                    c * square_size, r * square_size, square_size, square_size
                )
                pygame.draw.rect(screen, color, rect)

                piece = board[r][c]
                if piece is not None:
                    if piece in piece_images:
                        screen.blit(
                            piece_images[piece], (c * square_size, r * square_size)
                        )
                    else:
                        raise KeyError(f"Piece image not found for: {piece}")
