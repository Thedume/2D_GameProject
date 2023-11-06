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


def one_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_1    
    
    
class Idle:
    @staticmethod
    def enter(player, e):
        print("Enter Idle")
        player.dir = 0
        player.frame = 0
        player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)


class Hammer:
    pass


class Javelin:
    pass


class Hurdle:
    @staticmethod
    def enter(player, e):
        print("enter Hurdle State")
        player.action = 1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # player.frame = (player.frame + 1) % 8
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)

class Jump:
    @staticmethod
    def enter(player, e):
        if space_down(e):
            player.jump()

    @staticmethod
    def exit(player, e):
        if space_down(e):
            if space_down(e):
                if player.isJump > 0:
                    # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
                    if player.v > 0:
                        # 속도가 0보다 클때는 위로 올라감
                        F = (0.5 * player.m * (player.v * player.v))
                    else:
                        # 속도가 0보다 작을때는 아래로 내려감
                        F = -(0.5 * player.m * (player.v * player.v))

                    # 좌표 수정 : 위로 올라가기 위해서는 y 좌표를 줄여준다.
                    player.y -= round(F)

                    # 속도 줄여줌
                    player.v -= 1

                    # 바닥에 닿았을때, 변수 리셋
                    if player.rect.bottom > 90:
                        player.rect.bottom = 90
                        player.isJump = 0
                        player.v = 2

                player.dir_y = 0

        pass

    @staticmethod
    def do(player):
        # player.frame = (player.frame + 1) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)


class StateMachine:
    def __init__(self, player, _type):
        self.player = player
        if _type == 1:
            self.cur_state = Hurdle
        elif _type == 2:
            self.cur_state = Hammer
        elif _type == 3:
            self.cur_state = Javelin
        else:
            self.cur_state = Idle
        self.transitions = {
            Idle: {one_down: Hurdle},
            Hurdle: {one_down: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self, _type):
        self.x, self.y = 50, 90
        self.frame = 0
        self.action = 3
        self.image = load_image("./resources/animation_sheet.png")
        self.font = load_font("./resources/ENCR10B.TTF", 16)
        self.frame_time = 0.0
        self.dir_y = 0
        self.state_machine = StateMachine(self, _type)
        self.state_machine.start()

        self.isJump = 0
        self.v = 7
        self.m = 2



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