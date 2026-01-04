import os

import pygame

from config import COLORS, PIECE_COLORS, PIECE_TYPES, PIECES_DIR
from engine.board_manager import BoardManager
from engine.game_state import GameState
from engine.move_validator import MoveValidator


class ChessEngine:
    """Main chess engine that coordinates all game components"""

    def __init__(self, board=None):
        """Initialize chess engine with all modular components"""
        # Initialize core components
        self.board_manager = BoardManager(board)
        self.game_state = GameState()
        self.move_validator = MoveValidator(self.board_manager, self.game_state)

    def select_piece(self, row, col):
        """Select a piece at the given position if it belongs to current player"""
        if self.game_state.pawn_promotion:
            piece = self.board_manager.get_pawn_promotion_piece(row, col)
            promo_piece = f"{self.game_state.current_player}{piece}"
            last_move = self.game_state.get_last_move()

            if last_move:
                last_move_pos = (last_move["to"][0], last_move["to"][1])
                self.board_manager.set_piece(
                    last_move_pos[0], last_move_pos[1], promo_piece
                )
                self.game_state.add_move(
                    last_move_pos, last_move_pos, promo_piece, "pawn_promotion"
                )
                self.game_state.pawn_promotion = False
                if self.move_validator.is_check_move(self.game_state.current_player):
                    self.game_state.game_status = (
                        "check_b"
                        if self.game_state.current_player == "w"
                        else "check_w"
                    )
                self.game_state.switch_player()

            return

        piece = self.board_manager.get_piece(row, col)
        if (
            piece
            and piece[0] == self.game_state.current_player
            and self.board_manager.is_position_valid(row, col)
        ):
            # Remove piece from board and select it
            self.board_manager.remove_piece(row, col)
            self.game_state.set_select_piece(piece, (row, col))

    def make_move(self, to_row, to_col):
        """Attempt to move selected piece to destination"""
        if not self.game_state.selected_piece:
            return

        self.game_state.set_capture_piece(
            self.board_manager.get_piece(to_row, to_col), (to_row, to_col)
        )

        selected_piece = self.game_state.selected_piece
        captured_piece = self.game_state.captured_piece
        from_pos = self.game_state.selected_pos
        to_pos = self.game_state.captured_pos
        print(
            f"\nChessEngine.make_move -- Selected Piece: {selected_piece} -- Starting Pos: {from_pos} -- Ending Piece: {captured_piece} -- Ending Pos: {to_pos}"
        )

        if from_pos != to_pos and self.move_validator.is_valid_move(from_pos, to_pos):
            # Check if game is in 'check' state
            if self.game_state.game_status in ["check_b", "check_w"]:
                print(
                    "ChessEngine.make_move: Game state is in check. Game_state: ",
                    self.game_state.game_status,
                )
                if (
                    selected_piece[1] == "K"
                    and captured_piece
                    and captured_piece[1] == "R"
                ):
                    self.cancel_selection()
                    return
                self.board_manager.set_piece(to_row, to_col, selected_piece)
                self.game_state.clear_selection()
                if self.move_validator.is_remove_check(self.game_state.current_player):
                    self.game_state.game_status = "active"
                    self.game_state.add_move(
                        from_pos, to_pos, selected_piece, captured_piece
                    )
                else:
                    self.board_manager.remove_piece(to_row, to_col)
                    self.board_manager.set_piece(
                        from_pos[0], from_pos[1], selected_piece
                    )
                    self.board_manager.set_piece(to_pos[0], to_pos[1], captured_piece)
                    return
            # Determine if this is a castle move and make the move
            elif (
                selected_piece[1] == "K" and captured_piece and captured_piece[1] == "R"
            ):
                self.board_manager.handle_castle(selected_piece, from_pos, to_pos)
                self.game_state.add_move(from_pos, to_pos, "castle")
            # Make the move
            else:
                # Check if the move will leave current_player in 'check' state
                self.board_manager.set_piece(to_row, to_col, selected_piece)
                self.game_state.clear_selection()
                if not self.move_validator.is_remove_check(
                    self.game_state.current_player
                ):
                    self.board_manager.remove_piece(to_row, to_col)
                    self.board_manager.set_piece(
                        from_pos[0], from_pos[1], selected_piece
                    )
                    self.board_manager.set_piece(to_pos[0], to_pos[1], captured_piece)
                    return

                self.game_state.add_move(
                    from_pos, to_pos, selected_piece, captured_piece
                )
                if selected_piece[1] == "P" and (to_row == 0 or to_row == 7):
                    self.game_state.pawn_promotion = True

            # Update game state
            if not self.game_state.pawn_promotion:
                valid_moves = self.move_validator.get_all_valid_moves(
                    "b" if self.game_state.current_player == "w" else "w"
                )
                if self.move_validator.is_check_move(self.game_state.current_player):
                    self.game_state.game_status = (
                        "check_b"
                        if self.game_state.current_player == "w"
                        else "check_w"
                    )
                    # Check for checkmates
                    if len(valid_moves) == 0:
                        print(
                            f"Checkmate! Current player: {self.game_state.current_player} wins"
                        )
                        self.game_state.game_status = "complete"
                        return

                if len(valid_moves) == 0 and self.game_state.game_status not in [
                    "check_w",
                    "check_b",
                ]:
                    print("Stalemate!")
                    self.game_state.game_status = "draw"
                    return

                # Update castle state
                if (
                    self.game_state.can_castle()
                    and selected_piece[1] == "K"
                    or selected_piece[1] == "R"
                ):
                    self.game_state.set_castle()

                self.game_state.switch_player()
                self.game_state.clear_selection()
                self.game_state.clear_captured()

        else:
            self.cancel_selection()

    def cancel_selection(self):
        """Cancel current piece selection and return selected piece to original position"""
        if self.game_state.selected_piece:
            piece = self.game_state.selected_piece
            pos = self.game_state.selected_pos

            if pos:
                self.board_manager.set_piece(pos[0], pos[1], piece)

            self.game_state.clear_selection()
            self.game_state.clear_captured()

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

    def draw_pawn_promo(self, screen, piece_images, width, height):
        """Draw the pawn promotion popup"""
        popup_width, popup_height = 400, 100
        popup_x, popup_y = (width - popup_width) // 2, (height - popup_height) // 2
        promo_pieces = ["R", "N", "B", "Q"]

        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((255, 255, 255, 90))
        screen.blit(popup_surface, (popup_x, popup_y))
        rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            rect,
            3,
        )

        for i, piece_type in enumerate(promo_pieces):
            piece = self.game_state.current_player + piece_type

            screen.blit(
                piece_images[piece],
                (popup_x + (i * 100), popup_y),
            )

    def draw_winner(self, screen, piece_images, width, height):
        popup_width, popup_height = 400, 150
        popup_x, popup_y = (width - popup_width) // 2, (height - popup_height) // 2

        # Draw the background popup rectangle
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((255, 255, 255, 230))
        screen.blit(popup_surface, (popup_x, popup_y))
        rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        # Draw the border of the popup
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            rect,
            3,
        )

        # Get the king image
        king_image = piece_images[f"{self.game_state.current_player}K"]
        king_width = king_image.get_width()
        king_height = king_image.get_height()

        # Center the king image vertically in popup, position it left of center
        king_x = popup_x + (popup_width // 2) - 80
        king_y = popup_y + (popup_height - king_height) // 2
        screen.blit(king_image, (king_x, king_y))

        # Create and render the "WINS!" text
        font = pygame.font.Font(None, 48)
        text_color = (0, 0, 0)
        text_surface = font.render("WINS!", True, text_color)

        # Position text to the right of the king
        text_x = king_x + king_width + 20
        text_y = popup_y + (popup_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def draw_draw(self, screen, width, height):
        popup_width, popup_height = 400, 150
        popup_x, popup_y = (width - popup_width) // 2, (height - popup_height) // 2

        # Draw the background popup rectangle
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((255, 255, 255, 230))
        screen.blit(popup_surface, (popup_x, popup_y))
        rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        # Draw the border of the popup
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            rect,
            3,
        )

        # Create and render the "DRAW!" text
        font = pygame.font.Font(None, 48)
        text_color = (0, 0, 0)
        text_surface = font.render("DRAW!", True, text_color)

        text_x = popup_x + 150
        text_y = popup_y + (popup_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
