import sys

import pygame

from src.config import FPS, HEIGHT, SQUARE_SIZE, WIDTH
from src.engine.chess_engine import ChessEngine
from src.startup import draw_board, init_pygame, load_piece_images


def main():
    try:
        # Initialize pygame
        screen = init_pygame(WIDTH, HEIGHT, "Chess")

        # Load piece images
        piece_images = load_piece_images(SQUARE_SIZE)

        # Initialize chess game
        game = ChessEngine()

        clock = pygame.time.Clock()
        running = True
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
                        game.select_piece(row, col)
                    except (IndexError, TypeError, ZeroDivisionError) as e:
                        print(f"Invalid mouse click position: {e}")
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if game.game_state.has_selected_piece():
                        try:
                            row, col = mouse_y // SQUARE_SIZE, mouse_x // SQUARE_SIZE
                            game.make_move(row, col)
                        except (IndexError, TypeError, ZeroDivisionError) as e:
                            print(f"Invalid mouse release position: {e}")
                            game.cancel_selection()

            # Draw the board and all the changes that happened
            draw_board(screen, game.board_manager.board, piece_images, SQUARE_SIZE)

            # Keeps the piece image in the center of mouse cursor
            if game.game_state.has_selected_piece():
                try:
                    img = piece_images[game.game_state.get_selected_piece()]
                    x_offset = img.get_width() // 2
                    y_offset = img.get_height() // 2
                    screen.blit(img, (mouse_x - x_offset, mouse_y - y_offset))
                except KeyError as e:
                    print(f"Missing piece image: {e}")
                    # Reset selected piece to avoid continuous errors
                    game.cancel_selection()

            pygame.display.flip()
    except Exception as e:
        print("Error: ", e)
    finally:
        print(f"Move History: {game.game_state.get_move_history()}")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
