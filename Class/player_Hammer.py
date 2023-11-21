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
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(hammerPlayer, e):
        hammerPlayer.dir = 0
        hammerPlayer.frame = 0
        hammerPlayer.wait_time = get_time()
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.image.clip_draw(int(hammerPlayer.frame) * 100, hammerPlayer.action * 100, 100, 100, hammerPlayer.x,
                                     hammerPlayer.y)

class StateMachine:
    def __init__(self, hammerPlayer):
        print("StateMachine __init__")
        self.hammerPlayer = hammerPlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {}
        }

    def start(self):
        self.cur_state.enter(self.hammerPlayer, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hammerPlayer)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hammerPlayer, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hammerPlayer, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.hammerPlayer)


class HammerPlayer:
    def __init__(self):
        self.x, self.y = 120, 150
        self.frame = 0
        self.action = 3
        self.image = load_image("./resources/Hurdle/animation_sheet.png")
        self.font = load_font("./resources/ENCR10B.TTF", 16)
        self.isShowExplain = True
        self.frame_time = 0.0
        self.dir_y = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.meter = 0.0

        self.isJump = 0
        self.v = 7
        self.m = 2

        self.isDown = False

    def jump(self, j):
        self.isJump = j

    def update(self):
        self.state_machine.update()
        self.meter = RUN_SPEED_MPS * self.frame_time

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            self.isShowExplain = False
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 10, self.y + 50, f'{self.meter:02f}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        if group == 'player:hurdle':
            print("collision Hurdle")
            self.isDown = True