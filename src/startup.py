import pygame
import os
from config import PIECE_COLORS, PIECE_TYPES, PIECES_DIR, COLORS


def load_piece_images(square_size):
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


def init_pygame(width, height, title="Chess"):
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


def draw_board(screen, board, piece_images, square_size):
    """Draw the chess board with pieces."""
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
                    screen.blit(piece_images[piece], (c * square_size, r * square_size))
                else:
                    raise KeyError(f"Piece image not found for: {piece}")
