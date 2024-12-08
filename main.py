import pygame
import sys
import os

# Window settings
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

piece_images = {}
colors = ['w', 'b']
piece_types = ['K', 'Q', 'R', 'B', 'N', 'P']

# Load piece images and store in a dict 
for c in colors:
    for p in piece_types:
        piece_code = c + p
        filename = f"{piece_code}.png"
        path = os.path.join("assets", "pieces", filename)
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
            piece_images[piece_code] = img
        else:
            print(f"Warning: Image {filename} not found at {path}")

# Define initial board layout
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

def draw_board(surface, board):
    colors = [(240, 217, 181), (181, 136, 99)]  # light, dark squares
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect)
            
            piece = board[r][c]
            if piece is not None:
                surface.blit(piece_images[piece], (c * SQUARE_SIZE, r * SQUARE_SIZE))

def main():
    clock = pygame.time.Clock()
    running = True
    selected_piece = None
    selected_piece_pos = None
    mouse_x, mouse_y = 0, 0

    while running:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse Drag and Drop 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if board[row][col] is not None:
                    selected_piece = board[row][col]
                    selected_piece_pos = (row, col)
                    board[row][col] = None
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece is not None:
                    row, col = mouse_y // SQUARE_SIZE, mouse_x // SQUARE_SIZE
                    # Drop piece (no legality check yet)
                    board[row][col] = selected_piece
                    selected_piece = None
                    selected_piece_pos = None

        # Draw the board and all the changes that happened
        draw_board(screen, board)

        # Keeps the piece image in the center of mouse cursor
        if selected_piece is not None:
            img = piece_images[selected_piece]
            x_offset = img.get_width() // 2
            y_offset = img.get_height() // 2
            screen.blit(img, (mouse_x - x_offset, mouse_y - y_offset))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
