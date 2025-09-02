from src.config import INITIAL_BOARD


class BoardManager:
    """Manages the chess board state and basic operations"""

    def __init__(self, board=None):
        """Initialize board with given state or default starting position"""
        self.board = [row[:] for row in (board or INITIAL_BOARD)]

    def get_piece(self, row, col):
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, row, col, piece):
        """Place piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    def remove_piece(self, row, col):
        """Remove piece from given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board[row][col]
            self.board[row][col] = None
            return piece
        return None

    def move_piece(self, from_pos, to_pos):
        """Move piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.remove_piece(from_row, from_col)
        if piece:
            self.set_piece(to_row, to_col, piece)
            return True
        return False

    def is_position_valid(self, row, col):
        """Check if position is within board boundaries"""
        return 0 <= row < 8 and 0 <= col < 8

    def is_position_empty(self, row, col):
        """Check if position is empty"""
        return self.get_piece(row, col) is None

    def get_board_copy(self):
        """Return a deep copy of the current board state"""
        return [row[:] for row in self.board]

    def reset_board(self):
        """Reset board to initial starting position"""
        self.board = [row[:] for row in INITIAL_BOARD]

    def get_pieces_for_player(self, player_color):
        """Get all pieces for a given player ('w' or 'b')"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece[0] == player_color:
                    pieces.append(((row, col), piece))
        return pieces
