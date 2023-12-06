from pico2d import *

import server


class Score:
    def __init__(self):
        self.show_score = load_font("./resources/Giants-Inline.TTF", 16)

    def draw(self):
        self.show_score.draw(10, 200, "Player1 SCORE!", (0, 0, 0))
        self.show_score.draw(10, 150, f"1 : {server.f_player_score[server.game][0]}", (0, 0, 0))
        self.show_score.draw(10, 100, f"2 : {server.f_player_score[server.game][1]}", (0, 0, 0))
        self.show_score.draw(10, 50, f"3 : {server.f_player_score[server.game][2]}", (0, 0, 0))

        self.show_score.draw(160, 200, "Player2 SCORE!", (0, 0, 0))
        self.show_score.draw(160, 150, f"1 : {server.s_player_score[server.game][0]}", (0, 0, 0))
        self.show_score.draw(160, 100, f"2 : {server.s_player_score[server.game][1]}", (0, 0, 0))
        self.show_score.draw(160, 50, f"3 : {server.s_player_score[server.game][2]}", (0, 0, 0))

    def update(self):
        pass