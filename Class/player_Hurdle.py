from pico2d import *

import game_framework
import game_world
import server
from Class.hurdle import Hurdle
from Class.score import Score

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


def jump_end(e):
    return e[0] == 'JUMP_END'


def arrive(e):
    return e[0] == 'ARRIVE'


def time_out(e):
    return e[0] == 'TIME_OUT'


hurdle_distance = [13.72, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 14.02]
h_pix_distance = []
dis = 0
for distance in hurdle_distance:
    dis += distance * 33
    h_pix_distance.append(dis)


class Idle:
    @staticmethod
    def enter(hurdlePlayer, e):
        dis = 0
        for distance in h_pix_distance:
            server.hurdles.append(Hurdle(distance))
        game_world.add_objects(server.hurdles, 1)
        for hurdle in server.hurdles:
            game_world.add_collision_pair('player:hurdle', None, hurdle)

        hurdlePlayer.dir = 0
        hurdlePlayer.frame = 0
        hurdlePlayer.info_message = load_font("./resources/Giants-Inline.TTF", 32)
        hurdlePlayer.wait_time = get_time()
        pass

    @staticmethod
    def exit(hurdlePlayer, e):
        pass

    @staticmethod
    def do(hurdlePlayer):
        hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.info_message.draw(200, 425, "Press 'Space' to Start", (0, 0, 0))
        hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)


class Run:
    @staticmethod
    def enter(hurdlePlayer, e):
        # print("Enter Run")
        hurdlePlayer.action = 1
        for hurdle in server.hurdles:
            hurdle.isMove = True

    @staticmethod
    def exit(hurdlePlayer, e):
        pass

    @staticmethod
    def do(hurdlePlayer):
        hurdlePlayer.x += hurdlePlayer.dir * RUN_SPEED_PPS * game_framework.frame_time

        if hurdlePlayer.x >= 4000:
            print("arrive")
            hurdlePlayer.state_machine.handle_event(('ARRIVE', 0))
        # hurdlePlayer.x = clamp(25, hurdlePlayer.x, 1600 - 25)
        hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        # hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hurdlePlayer):
        if not hurdlePlayer.isDown:
            hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)
        elif hurdlePlayer.isDown:
            hurdlePlayer.image.clip_composite_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, -3.141592 / 1.75, '', hurdlePlayer.x, hurdlePlayer.y, 100, 100)
            # self, left, bottom, width, height, rad, flip, x, y, w = None, h = None


class Jump:
    @staticmethod
    def enter(hurdlePlayer, e):
        # print("Enter Jump")
        hurdlePlayer.wait_time = get_time()
        hurdlePlayer.isDown = False
        hurdlePlayer.dir_y = 1
        hurdlePlayer.player_jump_sound.play()

    @staticmethod
    def exit(hurdlePlayer, e):
        if space_down(e):
            pass

    @staticmethod
    def do(hurdlePlayer):
        # hurdlePlayer.frame = (hurdlePlayer.frame + 1) % 8
        hurdlePlayer.x += hurdlePlayer.dir * RUN_SPEED_PPS * game_framework.frame_time
        hurdlePlayer.x = clamp(25, hurdlePlayer.x, 1600 - 25)
        hurdlePlayer.frame = (hurdlePlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # print(hurdlePlayer.y)
        hurdlePlayer.y += hurdlePlayer.dir_y * 1
        if hurdlePlayer.y >= 300:
            hurdlePlayer.dir_y *= -1
        if hurdlePlayer.y < 150:
            hurdlePlayer.y = 150
            hurdlePlayer.state_machine.handle_event(('JUMP_END', 0))
        # delay(0.01)
        #  if get_time() - hurdlePlayer.wait_time > 1:
        #     hurdlePlayer.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)


class Showscore:
    @staticmethod
    def enter(hurdlePlayer, e):
        # print('Enter ShowScore')
        hurdlePlayer.frame = 0

        hurdlePlayer.score_message = load_font("./resources/Giants-Regular.TTF", 32)
        if hurdlePlayer.state == 'FIRST':
            server.f_player_score[server.game][0] = 10 - hurdlePlayer.down_count
        elif hurdlePlayer.state == 'SECOND':
            server.s_player_score[server.game][0] = 10 - hurdlePlayer.down_count

    @staticmethod
    def exit(hurdlePlayer, e):
        server.hurdles = None

    @staticmethod
    def do(hurdlePlayer):
        pass

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.score_message.draw(server.hammer.x, server.hammer.y + 10, "%.2f"%(server.hammer.x + server.background_hammer.window_left - 70), (255, 0, 0))

        hurdlePlayer.image.clip_draw(int(hurdlePlayer.frame) * 100, hurdlePlayer.action * 100, 100, 100, hurdlePlayer.x, hurdlePlayer.y)


class GameEnd:
    @staticmethod
    def enter(hurdlePlayer, e):
        hurdlePlayer.x, hurdlePlayer.y = 30, 380  # default : 10, 380
        hurdlePlayer.frame = 0
        hurdlePlayer.motion_state = 'Stop'
        hurdlePlayer.dir = 0
        hurdlePlayer.frame_time = 0.0
        hurdlePlayer.wait_time = get_time()

        hurdlePlayer.winner_message = load_font("./resources/Giants-Regular.TTF", 32)
        hurdlePlayer.score_message = Score()
        game_world.add_object(hurdlePlayer.score_message)
        hurdlePlayer.info_message = load_font("./resources/Giants-Regular.TTF", 32)

    @staticmethod
    def exit(hurdlePlayer, e):
        game_world.remove_object(hurdlePlayer.score_message)
        server.f_player_score[server.game] = [0 for i in range(1)]
        server.s_player_score[server.game] = [0 for i in range(1)]

    @staticmethod
    def do(hurdlePlayer):
        pass

    @staticmethod
    def draw(hurdlePlayer):
        hurdlePlayer.images[hurdlePlayer.motion_state][hurdlePlayer.frame].draw(hurdlePlayer.x, hurdlePlayer.y, 55, 55)

        if server.f_player_score[server.game][0] > server.s_player_score[server.game][0]:
            hurdlePlayer.winner_message.draw(300, 375, "PLAYER1 Win!!", (0, 0, 0))
        elif server.f_player_score[server.game][0] == server.s_player_score[server.game][0]:
            hurdlePlayer.winner_message.draw(300, 375, "Draw", (0, 0, 0))
        elif server.f_player_score[server.game][0] < server.s_player_score[server.game][0]:
            hurdlePlayer.winner_message.draw(300, 375, "PLAYER2 Win!!", (0, 0, 0))

        hurdlePlayer.info_message.draw(10, 550, "Press 'Space' to Restart", (255, 0, 0))


class StateMachine:
    def __init__(self, hurdlePlayer):
        self.hurdlePlayer = hurdlePlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {space_down: Run},
            Run: {space_down: Jump, s_down: Idle, arrive: Showscore},
            Jump: {jump_end: Run},
            Showscore: {space_down: Idle},
            GameEnd: {space_down: Idle}
        }

    def start(self):
        self.cur_state.enter(self.hurdlePlayer, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hurdlePlayer)

    def handle_event(self, e):
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
    player_jump_sound = None

    def __init__(self):
        self.x, self.y = 120, 150
        self.frame = 0
        self.action = 3
        self.image = load_image("./resources/Hurdle/animation_sheet.png")
        self.font = load_font("./resources/ENCR10B.TTF", 16)
        self.isShowExplain = True
        self.frame_time = 0.0
        self.dir_y = 0
        self.down_count = 0

        server.hurdles = []
        self.x_position = 0

        if not HurdlePlayer.player_jump_sound:
            HurdlePlayer.player_jump_sound = load_wav('./resources/sound/jump.mp3')
            HurdlePlayer.player_jump_sound.set_volume(32)

        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.meter = 0.0

        self.isDown = False

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            self.isShowExplain = False
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x-10, self.y + 50, f'{self.meter:02f}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        if group == 'player:hurdle':
            self.isDown = True
            self.down_count += 1
