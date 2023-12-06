from pico2d import *

import server


class Pannel:
    def __init__(self):
        self.show_menu = load_font("./resources/Giants-Inline.TTF", 32)

    def draw(self):
        self.show_menu.draw(300, 500, "Press 'Space' to Start", (0, 0, 0))

    def update(self):
        pass
