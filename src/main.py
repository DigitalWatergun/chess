import pygame
import sys

from startup import load_piece_images, draw_board, init_pygame
from config import WIDTH, HEIGHT, BOARD_SIZE, SQUARE_SIZE, FPS, INITIAL_BOARD
from engine.chess_engine import check_valid

# Create a copy of the initial board for the game
board = [row[:] for row in INITIAL_BOARD]


def main():
    try:
        # Initialize pygame
        screen = init_pygame(WIDTH, HEIGHT, "Chess")

        # Load piece images
        piece_images = load_piece_images(SQUARE_SIZE)

        clock = pygame.time.Clock()
        running = True
        selected_piece = None
        selected_piece_pos = None
        mouse_x, mouse_y = 0, 0

        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                # print("Event Type: ", pygame.event.event_name(event.type))
                if event.type == pygame.QUIT:
                    running = False

                # Mouse Drag and Drop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    try:
                        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                        # Bounds checking
                        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                            if board[row][col] is not None:
                                selected_piece = board[row][col]
                                selected_piece_pos = (row, col)
                                board[row][col] = None
                    except (IndexError, TypeError, ZeroDivisionError) as e:
                        print(f"Invalid mouse click position: {e}")
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_piece is not None:
                        try:
                            row, col = mouse_y // SQUARE_SIZE, mouse_x // SQUARE_SIZE
                            # Bounds checking
                            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                                if check_valid(
                                    board,
                                    selected_piece,
                                    selected_piece_pos,
                                    (row, col),
                                ):
                                    board[row][col] = selected_piece
                                else:
                                    # Return piece to original position
                                    if selected_piece_pos is not None:
                                        board[selected_piece_pos[0]][
                                            selected_piece_pos[1]
                                        ] = selected_piece
                            else:
                                # Out of bounds - return piece to original position
                                if selected_piece_pos is not None:
                                    board[selected_piece_pos[0]][
                                        selected_piece_pos[1]
                                    ] = selected_piece
                        except (IndexError, TypeError, ZeroDivisionError) as e:
                            print(f"Invalid mouse release position: {e}")
                            # Return piece to original position on error
                            if selected_piece_pos is not None:
                                board[selected_piece_pos[0]][
                                    selected_piece_pos[1]
                                ] = selected_piece
                        finally:
                            selected_piece = None
                            selected_piece_pos = None

            # Draw the board and all the changes that happened
            draw_board(screen, board, piece_images, SQUARE_SIZE)

            # Keeps the piece image in the center of mouse cursor
            if selected_piece is not None:
                try:
                    img = piece_images[selected_piece]
                    x_offset = img.get_width() // 2
                    y_offset = img.get_height() // 2
                    screen.blit(img, (mouse_x - x_offset, mouse_y - y_offset))
                except KeyError as e:
                    print(f"Missing piece image: {e}")
                    # Reset selected piece to avoid continuous errors
                    selected_piece = None
                    selected_piece_pos = None

            pygame.display.flip()
    except Exception as e:
        print("Error: ", e)
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
