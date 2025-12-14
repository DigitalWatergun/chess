from config import INITIAL_BOARD


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

    def is_position_valid(self, row, col):
        """Check if position is within board boundaries"""
        return 0 <= row < 8 and 0 <= col < 8

    def reset_board(self):
        """Reset board to initial starting position"""
        self.board = [row[:] for row in INITIAL_BOARD]

    def handle_castle(self, king, from_pos, to_pos):
        """Place pieces in the castle position"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        rook = self.remove_piece(to_row, to_col)
        if abs(from_col - to_col) == 4:
            self.set_piece(from_row, from_col - 2, king)
            self.set_piece(to_row, to_col + 3, rook)
        elif abs(from_col - to_col) == 3:
            self.set_piece(from_row, from_col + 2, king)
            self.set_piece(to_row, from_col + 1, rook)

    def get_pawn_promotion_piece(self, row, col):
        if row not in [3, 4] and col not in [2, 3, 4, 5]:
            return None

        if col == 2:
            return "R"
        elif col == 3:
            return "N"
        elif col == 4:
            return "B"
        elif col == 5:
            return "Q"

    def get_player_pieces(self, player):
        player_pieces = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col][0] == player:
                    player_pieces.append([self.board[row][col], row, col])

        return player_pieces

    def get_player_king_pos(self, player):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col] == player + "K":
                    return (row, col)
