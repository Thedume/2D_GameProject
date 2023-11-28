from pico2d import *


class Angle:
    def __init__(self, x, y):
        self.angle_img = load_image('./resources/hammer/angle.png') # 이미지 수정해야함
        self.arrow = load_image('./resources/hammer/arrow.png')
        self.x, self.y = x, y
        self.deg = 15 # -15 ~ 15
        self.isRotate = True

    def update(self):
        if not (-15 <= self.deg <= 15):
            pass # 파울
        if self.isRotate:
            self.deg += 0.5

        pass

    def draw(self):
        self.angle_img.draw(self.x, self.y, 50, 50)
        self.arrow.composite_draw(3.141592 / 180 * self.deg, '', self.x, self.y) #