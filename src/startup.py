#!/usr/bin/env python3
"""Chess Game Launcher

Run this file to start the chess game:
    python src/startup.py
    poetry run python src/startup.py
"""

import sys
from pathlib import Path

# Add src directory to Python path (startup.py is now in src/)
HERE = Path(__file__).parent  # /repo/src

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Import and run main
from main import main

if __name__ == "__main__":
    main()
