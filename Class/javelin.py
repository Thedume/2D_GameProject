from pico2d import *

import game_world


def calculate_position(angle, force, time, x, y):
    # 초기 속도 계산
    velocity_x = force * math.cos(math.radians(angle))
    velocity_y = force * math.sin(math.radians(angle))

    # 위치 계산
    x = (velocity_x * time) * 0.005 + x
    y = ((velocity_y * time) - (0.5 * 9.8 * time**2)) * 0.005 + y  # 중력 가속도 고려

    return x, y


class Javelin:
    def __init__(self, x, y, a, p):
        self.javelin_img = load_image('./resources/javelin/javelin.png')
        self.oy = y
        self.x, self.y = x, y
        self.angle, self.power = a, p
        self.isMove = False
        self.time = 0
        self.dt = 0.1
        self.state = 'move'

        # print(a, p)

    def update(self):
        if self.y >= self.oy and self.state == 'move':
            self.x, self.y = calculate_position(self.angle, self.power, self.time, self.x, self.y)
        else:
            self.state = 'stop'
        # print(self.x, self.y)
        self.angle -= self.dt
        self.time += self.dt
        delay(0.025)
        pass

    def draw(self):
        self.javelin_img.composite_draw(3.141592 / 180 * self.angle, '',self.x, self.y)
