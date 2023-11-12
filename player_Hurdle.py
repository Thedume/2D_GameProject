from pico2d import *

import game_framework

# self Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# self Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def space_down(e):
    print("space down")
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
    
    
class Idle:
    @staticmethod
    def enter(hurdlePlayer, e):
        print("Enter Idle")
        hurdlePlayer.dir = 0
        hurdlePlayer.frame = 0
        pass

    @staticmethod
    def exit(hurdlePlayer, e):
        pass

    @staticmethod
    def do(hurdlePlayer):
        hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)


class Run:
    @staticmethod
    def enter(hurdlePlayer, e):
        print("enter Hurdle State")
        hurdlePlayer.action = 1

    @staticmethod
    def exit(hurdlePlayer, e):
        if space_down(e):
            hurdlePlayer.jump(True)
            
        pass

    @staticmethod
    def do(hurdlePlayer):
        # hurdlePlayer.frame = (hurdlePlayer.frame + 1) % 8
        hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)


class Jump:
    @staticmethod
    def enter(hurdlePlayer, e):
        print("Enter Jump")
        if space_down(e):
            hurdlePlayer.jump(True)

    @staticmethod
    def exit(hurdlePlayer, e):
        if space_down(e):
            if hurdlePlayer.isJump:
                # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
                if hurdlePlayer.v > 0:
                    # 속도가 0보다 클때는 위로 올라감
                    F = (0.5 * hurdlePlayer.m * (hurdlePlayer.v * hurdlePlayer.v))
                else:
                    # 속도가 0보다 작을때는 아래로 내려감
                    F = -(0.5 * hurdlePlayer.m * (hurdlePlayer.v * hurdlePlayer.v))

                # 좌표 수정 : 위로 올라가기 위해서는 y 좌표를 줄여준다.
                hurdlePlayer.y -= round(F)

                # 속도 줄여줌
                hurdlePlayer.v -= 1

                # 바닥에 닿았을때, 변수 리셋
                if hurdlePlayer.rect.bottom > 90:
                    hurdlePlayer.rect.bottom = 90
                    hurdlePlayer.isJump = False
                    hurdlePlayer.v = 2

            hurdlePlayer.dir_y = 0

        hurdlePlayer.jump(False)

    @staticmethod
    def do(hurdlePlayer):
        # hurdlePlayer.frame = (hurdlePlayer.frame + 1) % 8
        hurdlePlayer.x += hurdlePlayer.dir * RUN_SPEED_PPS * game_framework.frame_time
        hurdlePlayer.x = clamp(25, hurdlePlayer.x, 1600 - 25)
        hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)


class StateMachine:
    def __init__(self, hurdlePlayer):
        self.hurdlePlayer = hurdlePlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {space_down: Run},
            Run: {space_down: Idle, s_down: Idle},
            Jump: {}
        }

    def start(self):
        self.cur_state.enter(self.hurdlePlayer, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hurdlePlayer)

    def handle_event(self, e):
        print("Handle_event")
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hurdlePlayer, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hurdlePlayer, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.hurdlePlayer)


class HurdlePlayer:
    def __init__(self):
        self.x, self.y = 50, 90
        self.frame = 0
        self.action = 3
        self.image = load_image("./resources/Hurdle/animation_sheet.png")
        self.font = load_font("./resources/ENCR10B.TTF", 16)
        self.frame_time = 0.0
        self.dir_y = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.isJump = 0
        self.v = 7
        self.m = 2

    def jump(self, j):
        self.isJump = j

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        pass