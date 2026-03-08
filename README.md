# Chess

A chess engine and game built from scratch with Pygame. Written offline without AI or internet assistance.

## Features

- All standard piece movements (pawn, rook, knight, bishop, queen, king)
- Check, checkmate, and stalemate detection
- Castling
- Pawn promotion
- Draw detection (fifty-move rule, threefold repetition, insufficient material)
- Drag-and-drop piece movement
- Game reset (Ctrl+R)

## Prerequisites

- Python 3.13 (managed via pyenv)
- Poetry

## Setup

```bash
# Install Python 3.13 via pyenv
pyenv install 3.13.9

# Install dependencies
poetry env use $(pyenv which python)
poetry install
```

## Run

```bash
poetry run python3 src/main.py
```

## Project Structure

```
src/
├── main.py                 # Game loop and Pygame event handling
├── config.py               # Board layout, colors, constants
├── assets/pieces/          # Piece images (bK.png, wP.png, etc.)
└── engine/
    ├── chess_engine.py     # Game orchestrator + rendering
    ├── board_manager.py    # Board state and piece operations
    ├── game_state.py       # Turn tracking, move history, selections
    ├── move_validator.py   # Move legality and check detection
    └── rules_engine.py     # Draw condition detection
```

## Roadmap

- [ ] En passant
- [ ] Separate rendering from game logic
- [ ] Player vs AI (minimax with alpha-beta pruning)
- [ ] Color selection and game management UI
