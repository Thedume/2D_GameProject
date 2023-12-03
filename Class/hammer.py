from pico2d import *


class Hammer:
    def __init__(self, x, y, a, p):
        self.hammer_img = load_image('./resources/hammer/hammer.png')
        self.x, self.y = x, y
        self.angle, self.power = a, p
        self.isMove = False

    def update(self):
            # # 초기 위치 설정
            # current_x, current_y = self.x, self.y
            #
            # # 각도를 라디안으로 변환
            # angle_rad = math.radians(self.angle)
            #
            # # 초기 속도 계산
            # initial_velocity_x = self.power * math.cos(angle_rad)
            # initial_velocity_y = self.power * math.sin(angle_rad)
            #
            # # 중력 가속도
            # gravity = 9.8
            #
            # # 시뮬레이션 시간 간격
            # time_step = 0.1
            #
            # # 시뮬레이션 진행
            #
            # # 현재 위치 업데이트
            # current_x += initial_velocity_x * time_step
            # current_y += initial_velocity_y * time_step - 0.5 * gravity * time_step ** 2
            #
            # # 현재 속도 업데이트
            # initial_velocity_y -= gravity * time_step
            #
            # # 결과 반환


        pass

    def draw(self):
        self.hammer_img.draw(self.x, self.y)