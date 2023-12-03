from pico2d import *


class Powerbar:
    def __init__(self, x, y, p):
        self.powerbar_img = load_image('./resources/hammer/powerbar.png') # 이미지 수정해야함
        self.x, self.y = x, y
        self.power = p
        self.p_dir = 1
        self.isUpDown = True

    def update(self):
        if self.isUpDown:
            if self.power >= 100 or self.power <= 1:
                self.p_dir *= -1
            self.power += self.p_dir * 0.5
        pass

    def draw(self):
        self.powerbar_img.draw(self.x, self.y, 50, self.power)