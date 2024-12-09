from engine.valid_moves import check_pawn_moves, check_rook_moves, check_king_moves

def check_valid(board, selected_piece, selected_piece_pos, dest_piece_pos): 
    # Check within boundaries
    if dest_piece_pos[0] < 0 or dest_piece_pos[0] > 7 or dest_piece_pos[1] < 0 or dest_piece_pos[1] > 7: 
        return False
    
    if selected_piece[1] == 'P':  
        return check_pawn_moves(selected_piece, selected_piece_pos, dest_piece_pos)
    
    if selected_piece[1] == 'R':
        return check_rook_moves(selected_piece_pos, dest_piece_pos)
    
    if selected_piece[1] == 'K':
        return check_king_moves(selected_piece_pos, dest_piece_pos)

    return False
