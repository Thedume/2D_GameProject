from pico2d import *

angle_state = {'hammer': 50, 'javelin': 30}


class Angle:
    def __init__(self, x, y, use):
        if use == 'hammer':
            self.angle_img = load_image('./resources/hammer/angle1.png')
        elif use == 'javelin':
            self.angle_img = load_image('./resources/hammer/angle2.png')
        self.arrow = load_image('./resources/hammer/arrow.png')
        self.x, self.y = x, y
        self.deg = 0 # -15 ~ 15 : Foul
        self.deg_dir = 1
        self.isRotate = True
        self.use = use
        self.size = angle_state[use]

    def update(self):
        match self.use:
            case 'hammer':
                if self.isRotate:
                    self.deg += 1.0
                    if self.deg == 360:
                        self.deg = 0
            case 'javelin':
                if self.isRotate:
                    self.deg += 0.5 * self.deg_dir
                    if (self.deg == 90.0 and self.deg_dir == 1) or (self.deg == 0.0 and self.deg_dir == -1):
                        self.deg_dir *= -1

    def draw(self):
        self.angle_img.draw(self.x, self.y, self.size, 50)
        self.arrow.composite_draw(3.141592 / 180 * self.deg, '', self.x, self.y)
