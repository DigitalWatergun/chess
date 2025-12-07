from engine.board_manager import BoardManager
from engine.game_state import GameState


class MoveValidator:
    """Handles all move validation logic"""

    def __init__(self, board_manager: BoardManager, game_state: GameState):
        """Initialize with reference to board manager"""
        self.board_manager = board_manager
        self.game_state = game_state

    def is_valid_move(self, to_pos):
        """Check if a move is valid according to chess rules"""
        if not self.game_state.selected_piece or not self.game_state.selected_pos:
            return False
        to_row, to_col = to_pos
        if not self.board_manager.is_position_valid(to_row, to_col):
            return False

        selected_piece = self.game_state.selected_piece
        piece_type = selected_piece[1]

        if piece_type == "P":
            return self._check_pawn_moves(selected_piece, to_pos)
        elif piece_type == "R":
            return self._check_rook_moves(to_pos)
        elif piece_type == "N":
            return self._check_knight_moves(to_pos)
        elif piece_type == "B":
            return self._check_bishop_moves(to_pos)
        elif piece_type == "Q":
            return self._check_queen_moves(to_pos)
        elif piece_type == "K":
            return self._check_king_moves(to_pos)

        return False

    def _check_pawn_moves(self, selected_piece, to_pos):
        start_row, start_col = self.game_state.selected_pos
        end_row, end_col = to_pos
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

    def _check_rook_moves(self, to_pos):
        start_row, start_col = self.game_state.selected_pos
        end_row, end_col = to_pos

        if start_row != end_row and start_col == end_col:
            return self._check_blocking_col_pieces(
                start_col, start_row, end_row, end_col
            )
        elif start_row == end_row and start_col != end_col:
            # TODO: If the blocking piece is a king and the king is the endpiece, and the game_state castle is true, return true here
            return self._check_blocking_row_pieces(
                start_row, start_col, end_row, end_col
            )
        return False

    def _check_knight_moves(self, to_pos):
        start_row, start_col = self.game_state.selected_pos
        end_row, end_col = to_pos
        end_piece = self.board_manager.get_piece(end_row, end_col)

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
                if not end_piece or (
                    end_piece and end_piece[0] != self.game_state.selected_piece[0]
                ):
                    return True

        return False

    def _check_bishop_moves(self, to_pos):
        start_row, start_col = self.game_state.selected_pos
        end_row, end_col = to_pos

        if abs(end_row - start_row) == abs(end_col - start_col):
            return self._check_blocking_diag_pieces(
                start_row, start_col, end_row, end_col
            )

        return False

    def _check_queen_moves(self, to_pos):
        start_row, start_col = self.game_state.selected_pos
        end_row, end_col = to_pos

        if start_row != end_row and start_col == end_col:
            return self._check_blocking_col_pieces(
                start_col, start_row, end_row, end_col
            )
        elif start_row == end_row and start_col != end_col:
            return self._check_blocking_row_pieces(
                start_row, start_col, end_row, end_col
            )
        elif abs(end_row - start_row) == abs(end_col - start_col):
            return self._check_blocking_diag_pieces(
                start_row, start_col, end_row, end_col
            )

        return False

    def _check_king_moves(self, to_pos):
        start_row, start_col = self.game_state.selected_pos
        end_row, end_col = to_pos
        end_piece = self.board_manager.get_piece(end_row, end_col)

        # Check if this is a castle move
        if (
            self.game_state.can_castle()
            and end_piece == self.game_state.current_player + "R"
            and self._check_blocking_castle_pieces(
                start_row, start_col, end_col, end_piece
            )
        ):
            return True

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

        # Check if all other moves are valid
        for dr, dc in directions:
            if start_row + dr == end_row and start_col + dc == end_col:
                if not end_piece or (
                    end_piece and end_piece[0] != self.game_state.selected_piece[0]
                ):
                    return True

        return False

    def _check_blocking_castle_pieces(self, start_row, start_col, end_col, end_piece):
        step = 1 if start_col < end_col else -1

        for col in range(start_col, end_col + step, step):
            blocking_piece = self.board_manager.get_piece(start_row, col)
            if blocking_piece:
                if blocking_piece == end_piece:
                    return True
                return False

    def _check_blocking_row_pieces(self, start_row, start_col, end_row, end_col):
        step = 1 if start_col < end_col else -1
        start_piece = self.game_state.selected_piece
        end_piece = self.board_manager.get_piece(end_row, end_col)

        for col in range(start_col, end_col + step, step):
            blocking_piece = self.board_manager.get_piece(start_row, col)
            if blocking_piece:
                if (
                    end_piece
                    and blocking_piece == end_piece
                    and start_piece[0] != end_piece[0]
                ):
                    return True
                return False
        return True

    def _check_blocking_col_pieces(self, start_col, start_row, end_row, end_col):
        step = 1 if start_row < end_row else -1
        start_piece = self.game_state.selected_piece
        end_piece = self.board_manager.get_piece(end_row, end_col)

        for row in range(start_row, end_row + step, step):
            blocking_piece = self.board_manager.get_piece(row, start_col)
            if blocking_piece:
                if (
                    end_piece
                    and blocking_piece == end_piece
                    and start_piece[0] != end_piece[0]
                ):
                    return True
                return False
        return True

    def _check_blocking_diag_pieces(self, start_row, start_col, end_row, end_col):
        start_piece = self.game_state.selected_piece
        end_piece = self.board_manager.get_piece(end_row, end_col)

        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1
        row, col = start_row, start_col
        blocking_piece = None

        for _ in range(abs(start_row - end_row)):
            row += row_step
            col += col_step
            blocking_piece = self.board_manager.get_piece(row, col)
            if blocking_piece:
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
