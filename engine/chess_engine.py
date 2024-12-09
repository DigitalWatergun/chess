import engine.valid_moves as valid_moves

def check_valid(board, selected_piece, selected_piece_pos, dest_piece_pos): 
    # Check within boundaries
    if dest_piece_pos[0] < 0 or dest_piece_pos[0] > 7 or dest_piece_pos[1] < 0 or dest_piece_pos[1] > 7: 
        return False
    
    if selected_piece[1] == 'P':  
        return valid_moves.check_pawn_moves(selected_piece, selected_piece_pos, dest_piece_pos)
    
    if selected_piece[1] == 'R':
        return valid_moves.check_rook_moves(selected_piece_pos, dest_piece_pos)
    
    if selected_piece[1] == 'N':
        return valid_moves.check_knight_moves(selected_piece_pos, dest_piece_pos) 
    
    if selected_piece[1] == 'B':
        return valid_moves.check_bishop_moves(selected_piece_pos, dest_piece_pos)
    
    if selected_piece[1] == 'Q':
        return valid_moves.check_queen_moves(selected_piece_pos, dest_piece_pos)
    
    if selected_piece[1] == 'K':
        return valid_moves.check_king_moves(selected_piece_pos, dest_piece_pos)
    


    return False
