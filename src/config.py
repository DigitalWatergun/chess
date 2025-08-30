# Game configuration constants

# Window settings
WIDTH = 480
HEIGHT = 480
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE  # 60

# Colors (RGB tuples)
COLORS = {"light_square": (122, 133, 147), "dark_square": (45, 53, 65)}

# Game settings
FPS = 120

# Piece types and colors
PIECE_COLORS = ["w", "b"]
PIECE_TYPES = ["K", "Q", "R", "B", "N", "P"]

# Asset paths
ASSETS_DIR = "src/assets"
PIECES_DIR = f"{ASSETS_DIR}/pieces"

# Initial board layout
INITIAL_BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
]
