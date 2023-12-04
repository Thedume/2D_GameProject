from pico2d import *


class Javelin:
    def __init__(self, x, y, a, p):
        self.javelin_img = load_image('./resources/javelin/javelin.png')
        self.x, self.y = x, y
        self.angle, self.power = a, p
        self.isMove = False

    def update(self):
        pass

    def draw(self):
        self.javelin_img.draw(self.x, self.y)