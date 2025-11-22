def check_pawn_moves(board, selected_piece, selected_piece_pos, dest_piece_pos):
    start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
    end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]
    end_piece = board[end_row][end_col]

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
        if (initial_pos == start_row and end_row == start_row + (2 * direction)) or (
            end_row == start_row + direction
        ):
            return True

    return False


def check_rook_moves(board, selected_piece, selected_piece_pos, dest_piece_pos):
    start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
    end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]
    end_piece = board[end_row][end_col]

    if end_piece and end_piece[0] == selected_piece[0]:
        return False
    elif start_row != end_row and start_col == end_col:
        return True
    elif start_row == end_row and start_col != end_col:
        return check_valid_row_moves(board, start_row, start_col, end_col)
    return False


def check_knight_moves(selected_piece_pos, dest_piece_pos):
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


def check_bishop_moves(selected_piece_pos, dest_piece_pos):
    start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
    end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

    return abs(end_row - start_row) == abs(end_col - start_col)


def check_queen_moves(selected_piece_pos, dest_piece_pos):
    start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
    end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

    if (
        abs(end_row - start_row) == abs(end_col - start_col)
        or (start_row != end_row and start_col == end_col)
        or (start_row == end_row and start_col != end_col)
    ):
        return True

    return False


def check_king_moves(selected_piece_pos, dest_piece_pos):
    start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
    end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

    for dr, dc in directions:
        if start_row + dr == end_row and start_col + dc == end_col:
            return True

    return False


def check_valid_row_moves(board, start_row, start_col, end_col):
    step = 1 if start_col < end_col else -1
    for col in range(start_col, end_col, step):
        blocking_piece = board[start_row][col]
        if blocking_piece:
            return False
    return True
