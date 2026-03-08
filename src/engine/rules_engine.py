from engine.board_manager import BoardManager
from engine.game_state import GameState


class RulesEngine:
    def __init__(self, board_manager: BoardManager, game_state: GameState):
        self.board_manager = board_manager
        self.game_state = game_state

    def is_fifty_move_draw(self):
        if len(self.game_state.move_history) < 50:
            return False

        # Move History: [{'from': (7, 6), 'to': (5, 5), 'piece': 'wN', 'captured': None, 'player': 'w'}]
        for i in range(0, 50, -1):
            move = self.game_state.move_history[i]
            if move["piece"][1] == "P" or move["captured"] is not None:
                return False

        return True

    def is_threefold_repetition_draw(self):
        for _, board_pos_count in self.board_manager.board_position_history.items():
            if board_pos_count >= 3:
                return True

        return False

    def is_insufficient_material_draw(self):
        b_player_pieces = self.board_manager.get_player_pieces("b")
        w_player_pieces = self.board_manager.get_player_pieces("w")
        all_player_pieces = set()

        insufficient_pieces = [
            {"bK", "wK"},
            {"bK", "bN", "wK"},
            {"wK", "wN", "bK"},
            {"bK", "bB", "wK"},
            {"wK", "wB", "bK"},
            {"bK", "bB", "wK", "wB"},
            {"wK", "wB", "bK", "bB"},
        ]

        for pieces in w_player_pieces:
            all_player_pieces.add(pieces[0])
        for pieces in b_player_pieces:
            all_player_pieces.add(pieces[0])

        def is_white_square(row, col):
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                return True
            return False

        def is_same_color_bishops(b_bishop, w_bishop):
            return is_white_square(b_bishop[1], b_bishop[2]) == is_white_square(
                w_bishop[1], w_bishop[2]
            )

        for pieces in insufficient_pieces:
            if pieces == all_player_pieces:
                if len(pieces) == 4:
                    bB = [piece for piece in b_player_pieces if piece[0][1] == "B"][0]
                    wB = [piece for piece in w_player_pieces if piece[0][1] == "B"][0]
                    return is_same_color_bishops(bB, wB)
                return True

        return False
