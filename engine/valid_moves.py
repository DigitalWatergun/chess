
def check_pawn_moves(board, selected_piece, selected_piece_pos, dest_piece_pos):
    start_row, start_col = selected_piece_pos[0], selected_piece_pos[1]
    end_row, end_col = dest_piece_pos[0], dest_piece_pos[1]

    if selected_piece == 'wP': 
        direction = -1
        initial_pos = 6
    else: 
        direction = 1
        initial_pos = 1

    if start_col == end_col: 
        if initial_pos == start_row and end_row == start_row + (2 * direction): 
            return True
        if end_row == start_row + direction: 
            return True

    return False
