from pico2d import *


class Angle:
    def __init__(self, x, y):
        self.angle_img = load_image('./resources/hammer/angle.png') # 이미지 수정해야함
        self.arrow = load_image('./resources/hammer/arrow.png')
        self.x, self.y = x, y
        self.deg = 0 # -15 ~ 15 : Foul
        self.isRotate = True

    def update(self):
        if self.isRotate:
            self.deg += 1.0
            if self.deg == 360:
                self.deg = 0

    def draw(self):
        self.angle_img.draw(self.x, self.y, 50, 50)
        self.arrow.composite_draw(3.141592 / 180 * self.deg, '', self.x, self.y)
