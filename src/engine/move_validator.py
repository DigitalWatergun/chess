class MoveValidator:
    """Handles all move validation logic"""

    def __init__(self, board_manager, game_state):
        """Initialize with reference to board manager"""
        self.board_manager = board_manager
        self.game_state = game_state

    def is_valid_move(self, piece, from_pos, to_pos):
        """Check if a move is valid according to chess rules"""
        # Check within boundaries
        to_row, to_col = to_pos
        if not self.board_manager.is_position_valid(to_row, to_col):
            return False

        piece_type = piece[1]

        if piece_type == "P":
            return self._check_pawn_moves(piece, from_pos, to_pos)
        elif piece_type == "R":
            return self._check_rook_moves(piece, from_pos, to_pos)
        elif piece_type == "N":
            return self._check_knight_moves(from_pos, to_pos)
        elif piece_type == "B":
            return self._check_bishop_moves(to_pos)
        elif piece_type == "Q":
            return self._check_queen_moves(from_pos, to_pos)
        elif piece_type == "K":
            return self._check_king_moves(from_pos, to_pos)

        return False

    def _check_pawn_moves(self, selected_piece, selected_piece_pos, dest_piece_pos):
        start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
        end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]
        end_piece = self.board_manager.get_piece(end_row, end_col)

        if selected_piece == "wP":
            direction = -1
            initial_pos = 6
        else:
            direction = 1
            initial_pos = 1

        col_diff = abs(end_col - start_col)
        row_diff = end_row - start_row

        # Check if diagonal capture movement
        if (
            col_diff == 1
            and row_diff == direction
            and end_piece is not None
            and end_piece != selected_piece
        ):
            return True
        # Check if vertical piece movement
        elif col_diff == 0 and end_piece is None:
            if (
                initial_pos == start_row and end_row == start_row + (2 * direction)
            ) or (end_row == start_row + direction):
                return True

        return False

    def _check_rook_moves(self, selected_piece, selected_piece_pos, dest_piece_pos):
        start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
        end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]
        end_piece = self.board_manager.get_piece(end_row, end_col)

        if end_piece and end_piece[0] == selected_piece[0]:
            return False
        elif start_row != end_row and start_col == end_col:
            return self._check_blocking_col_pieces(start_col, start_row, end_row)
        elif start_row == end_row and start_col != end_col:
            return self._check_blocking_row_pieces(start_row, start_col, end_col)
        return False

    def _check_knight_moves(self, selected_piece_pos, dest_piece_pos):
        start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
        end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

        directions = [
            [-2, 1],
            [-2, -1],
            [-1, 2],
            [-1, -2],
            [2, 1],
            [2, -1],
            [1, -2],
            [1, 2],
        ]

        for dr, dc in directions:
            if start_row + dr == end_row and start_col + dc == end_col:
                return True

        return False

    def _check_bishop_moves(self, dest_piece_pos):
        selected_piece_pos = self.game_state.get_selected_position()
        start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
        end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

        if abs(end_row - start_row) == abs(end_col - start_col):
            return self._check_blocking_diag_pieces(
                start_row, start_col, end_row, end_col
            )

        return False

    def _check_queen_moves(self, selected_piece_pos, dest_piece_pos):
        start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
        end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

        if (
            abs(end_row - start_row) == abs(end_col - start_col)
            or (start_row != end_row and start_col == end_col)
            or (start_row == end_row and start_col != end_col)
        ):
            return True

        return False

    def _check_king_moves(self, selected_piece_pos, dest_piece_pos):
        start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
        end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

        directions = [
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1],
        ]

        for dr, dc in directions:
            if start_row + dr == end_row and start_col + dc == end_col:
                return True

        return False

    def _check_blocking_row_pieces(self, start_row, start_col, end_col):
        step = 1 if start_col < end_col else -1
        for col in range(start_col, end_col, step):
            blocking_piece = self.board_manager.get_piece(start_row, col)
            if blocking_piece:
                return False
        return True

    def _check_blocking_col_pieces(self, start_col, start_row, end_row):
        step = 1 if start_row < end_row else -1
        for row in range(start_row, end_row, step):
            blocking_piece = self.board_manager.get_piece(row, start_col)
            if blocking_piece:
                return False
        return True

    def _check_blocking_diag_pieces(self, start_row, start_col, end_row, end_col):
        start_piece = self.game_state.get_selected_piece()
        end_piece = self.board_manager.get_piece(end_row, end_col)

        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1
        row, col = start_row, start_col
        blocking_piece = None

        for _ in range(abs(start_row - end_row)):
            row += row_step
            col += col_step
            blocking_piece = self.board_manager.get_piece(row, col)
            print(row, col, "Blocking Piece: ", blocking_piece)
            if blocking_piece is not None:
                break

        if blocking_piece:
            if (
                end_piece
                and blocking_piece == end_piece
                and start_piece[0] != end_piece[0]
            ):
                return True
            return False

        return True

    def get_all_legal_moves(self, player_color):
        """Get all legal moves for a given player"""
        legal_moves = []
        pieces = self.board_manager.get_pieces_for_player(player_color)

        for (row, col), piece in pieces:
            piece_moves = self.get_legal_moves_for_piece(row, col)
            for move in piece_moves:
                legal_moves.append(((row, col), move, piece))

        return legal_moves

    def get_legal_moves_for_piece(self, row, col):
        """Get all legal moves for a piece at given position"""
        piece = self.board_manager.get_piece(row, col)
        if not piece:
            return []

        legal_moves = []

        # Check all possible destinations on the board
        for to_row in range(8):
            for to_col in range(8):
                if (to_row, to_col) != (row, col):  # Don't include current position
                    if self.is_valid_move(piece, (row, col), (to_row, to_col)):
                        legal_moves.append((to_row, to_col))

        return legal_moves

    def can_piece_move(self, row, col):
        """Check if a piece at given position has any legal moves"""
        return len(self.get_legal_moves_for_piece(row, col)) > 0

    def is_move_blocked(self, from_pos, to_pos):
        """Check if path between positions is blocked (for sliding pieces)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Calculate direction
        row_dir = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_dir = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        # Check each square in the path (excluding start and end)
        current_row, current_col = from_row + row_dir, from_col + col_dir

        while (current_row, current_col) != (to_row, to_col):
            if not self.board_manager.is_position_empty(current_row, current_col):
                return True
            current_row += row_dir
            current_col += col_dir

        return False

    def is_capture_move(self, piece, to_pos):
        """Check if move is a capture (destination has opponent piece)"""
        to_row, to_col = to_pos
        target_piece = self.board_manager.get_piece(to_row, to_col)

        if target_piece and target_piece[0] != piece[0]:  # Different colors
            return True
        return False
