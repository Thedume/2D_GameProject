from pico2d import *


def calculate_position(angle, force, time):
    # 초기 속도 계산
    velocity_x = force * math.cos(math.radians(angle))
    velocity_y = force * math.sin(math.radians(angle))

    # 위치 계산
    x = velocity_x * time
    y = (velocity_y * time) - (0.5 * 9.8 * time**2)  # 중력 가속도 고려

    return x, y


class Javelin:
    def __init__(self, x, y, a, p):
        self.javelin_img = load_image('./resources/javelin/javelin.png')
        self.x, self.y = x, y
        self.angle, self.power = a, p
        self.isMove = False
        self.time = 0
        self.dt = 0.1

    def update(self):
        self.x, self.y = calculate_position(self.angle, self.power, self.time)

        self.time += self.dt
        pass

    def draw(self):
        self.javelin_img.draw(self.x, self.y)
