from pico2d import *

import game_world
import server
import Screen.score_screen
from Class.angle import Angle
from Class.javelin import Javelin
from Class.power_bar import Powerbar

import game_framework
from Class.score import Score

# self Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 3.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# self Action Speed
TIME_PER_ACTION = 6.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def time_out(e):
    return e[0] == 'TIME_OUT'


def foul(e):
    return e[0] == 'FOUL'


def end(e):
    return e[0] == 'END'


def game_end(e):
    return e[0] == 'GAME_END'


class Idle:
    @staticmethod
    def enter(jPlayer, e):
        global FRAMES_PER_ACTION
        jPlayer.x, jPlayer.y = 30, 380  # default : 10, 380
        jPlayer.frame = 0
        jPlayer.dir = 0
        jPlayer.frame_time = 0.0
        jPlayer.wait_time = get_time()

        jPlayer.info_message = load_font("./resources/Giants-Inline.TTF", 32)

        if jPlayer.chance == 0:
            game_framework.push_mode(Screen.score_screen)

            if server.player.state == 'SECOND':
                jPlayer.state_machine.handle_event(('GAME_END', 0))

            jPlayer.chance = 3

    @staticmethod
    def exit(jPlayer, e):
        pass

    @staticmethod
    def do(jPlayer):
        #jPlayer.frame = (jPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass

    @staticmethod
    def draw(jPlayer):
        if not (jPlayer.chance == 0):
            jPlayer.info_message.draw(200, 375, "Press 'Space' to Start", (0, 0, 0))
        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, jPlayer.x, jPlayer.y)


class Move:
    @staticmethod
    def enter(jPlayer, e):
        global FRAMES_PER_ACTION
        # print('Enter Move')

        pass

    @staticmethod
    def exit(jPlayer, e):
        if space_down(e):
            pass
        pass

    @staticmethod
    def do(jPlayer):
        jPlayer.x += RUN_SPEED_PPS * game_framework.frame_time
        jPlayer.frame = (jPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if jPlayer.x >= 160:
            # print("over")
            jPlayer.state_machine.handle_event(('FOUL', 0))

    @staticmethod
    def draw(jPlayer):
        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, jPlayer.x, jPlayer.y)


class CheckAngle:
    @staticmethod
    def enter(jPlayer, e):
        # print('Enter Angle')
        jPlayer.angle = Angle(jPlayer.x + 50, jPlayer.y + 5, 'javelin')
        game_world.add_object(jPlayer.angle, 2)
        pass

    @staticmethod
    def exit(jPlayer, e):
        if space_down(e):
            jPlayer.angle.isRotate = False
            jPlayer.angle_deg = jPlayer.angle.deg
            pass
        pass

    @staticmethod
    def do(jPlayer):
        # jPlayer.frame = (jPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass

    @staticmethod
    def draw(jPlayer):
        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, jPlayer.x, jPlayer.y)


class CheckPower:
    @staticmethod
    def enter(jPlayer, e):
        # print('Enter Power')

        jPlayer.powerbar = Powerbar(jPlayer.x + 100, jPlayer.y + 5, 2)
        game_world.add_object(jPlayer.powerbar, 2)
        pass

    @staticmethod
    def exit(jPlayer, e):
        if space_down(e):
            jPlayer.angle.isRotate = False
            jPlayer.powerbar_power = jPlayer.powerbar.power
            # print(jPlayer.powerbar_power)
        if jPlayer.angle:
            game_world.remove_object(jPlayer.angle)
        if jPlayer.powerbar:
            game_world.remove_object(jPlayer.powerbar)

    @staticmethod
    def do(jPlayer):
        # jPlayer.frame = (jPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass

    @staticmethod
    def draw(jPlayer):
        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, jPlayer.x, jPlayer.y)


class Stop:
    @staticmethod
    def enter(jPlayer, e):
        # print('Enter Stop')
        jPlayer.frame = 7
        server.javelin = Javelin(jPlayer.x, jPlayer.y, jPlayer.angle_deg, jPlayer.powerbar_power)
        game_world.add_object(server.javelin)

        # print(jPlayer.x, jPlayer.y)
        pass

    @staticmethod
    def exit(jPlayer, e):
        # game_world.remove_object(server.javelin)
        pass

    @staticmethod
    def do(jPlayer):
        if server.javelin.state == 'stop':
            jPlayer.state_machine.handle_event(('END', 0))
        pass

    @staticmethod
    def draw(jPlayer):
        sx, sy = jPlayer.x - server.background_j.window_left, jPlayer.y - server.background_j.window_bottom

        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, sx, sy)


class Showscore:
    @staticmethod
    def enter(jPlayer, e):
        # print('Enter ShowScore')
        jPlayer.frame = 7

        jPlayer.score_message = load_font("./resources/Giants-Regular.TTF", 32)
        if jPlayer.state == 'FIRST':
            server.f_player_score['hurdle'][3 - jPlayer.chance] = (round((server.javelin.x + server.background_j.window_left - 70), 2))
        elif jPlayer.state == 'SECOND':
            server.s_player_score['hurdle'][3 - jPlayer.chance] = (round((server.javelin.x + server.background_j.window_left - 70), 2))
        pass

    @staticmethod
    def exit(jPlayer, e):
        game_world.remove_object(server.javelin)
        server.javelin = None
        jPlayer.chance -= 1

    @staticmethod
    def do(jPlayer):
        pass

    @staticmethod
    def draw(jPlayer):
        jPlayer.score_message.draw(server.javelin.x, server.javelin.y + 10, "%.2f"%(server.javelin.x + server.background_j.window_left - 70), (255, 0, 0))

        sx, sy = jPlayer.x - server.background_j.window_left, jPlayer.y - server.background_j.window_bottom

        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, sx, sy)


class GameEnd:
    @staticmethod
    def enter(jPlayer, e):
        jPlayer.x, jPlayer.y = 30, 380  # default : 10, 380
        jPlayer.frame = 7
        jPlayer.dir = 0
        jPlayer.frame_time = 0.0
        jPlayer.wait_time = get_time()

        jPlayer.winner_message = load_font("./resources/Giants-Regular.TTF", 32)
        jPlayer.score_message = Score()
        game_world.add_object(jPlayer.score_message)
        jPlayer.info_message = load_font("./resources/Giants-Regular.TTF", 32)
        pass

    @staticmethod
    def exit(jPlayer, e):
        game_world.remove_object(jPlayer.score_message)
        server.f_player_score['hurdle'] = [0 for i in range(3)]
        server.s_player_score['hurdle'] = [0 for i in range(3)]

    @staticmethod
    def do(jPlayer):
        pass

    @staticmethod
    def draw(jPlayer):
        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, jPlayer.x, jPlayer.y)

        if max(server.f_player_score['hurdle']) > max(server.s_player_score['hurdle']):
            jPlayer.winner_message.draw(300, 375, "PLAYER1 Win!!", (0, 0, 0))
        elif max(server.f_player_score['hurdle']) == max(server.s_player_score['hurdle']):
            jPlayer.winner_message.draw(300, 375, "Draw", (0, 0, 0))
        elif max(server.f_player_score['hurdle']) < max(server.s_player_score['hurdle']):
            jPlayer.winner_message.draw(300, 375, "PLAYER2 Win!!", (0, 0, 0))

        jPlayer.info_message.draw(10, 550, "Press 'Space' to Restart", (255, 0, 0))


class Foul:
    @staticmethod
    def enter(jPlayer, e):
        # print('Enter Foul')
        jPlayer.frame = 0
        if jPlayer.state == 'FIRST':
            server.f_player_score['hurdle'][3 - jPlayer.chance] = 0
        elif jPlayer.state == 'SECOND':
            server.s_player_score['hurdle'][3 - jPlayer.chance] = 0

        jPlayer.foul_message = load_font("./resources/Giants-Inline.TTF", 32)
        pass

    @staticmethod
    def exit(jPlayer, e):
        jPlayer.chance -= 1

    @staticmethod
    def do(jPlayer):
        pass

    @staticmethod
    def draw(jPlayer):
        jPlayer.image.clip_draw(int(jPlayer.frame) * 51, 0, 51, 48, jPlayer.x, jPlayer.y)
        jPlayer.foul_message.draw(350, 300, "FOUL", (255, 0, 0))
        jPlayer.foul_message.draw(10, 550, "Press 'Space' to Restart", (0, 0, 0))


class StateMachine:
    def __init__(self, jPlayer):
        # print("StateMachine __init__")
        self.jPlayer = jPlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {space_down: Move, game_end: GameEnd},
            Move: {space_down: CheckAngle, foul: Foul},
            CheckAngle: {foul: Foul, space_down: CheckPower},
            CheckPower: {foul: Foul, space_down: Stop},
            Stop: {end: Showscore},
            Showscore : {space_down: Idle},
            Foul: {space_down: Idle},
            GameEnd : {space_down: Idle}
        }

    def start(self):
        self.cur_state.enter(self.jPlayer, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.jPlayer)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.jPlayer, e)
                self.cur_state = next_state
                self.cur_state.enter(self.jPlayer, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.jPlayer)


class JavelinPlayer:
    images = None

    def __init__(self):
        self.x, self.y = 30, 380 # default : 10, 380
        self.frame = 0
        self.image = load_image("./resources/javelin/player.png")
        self.frame_time = 0.0
        self.chance = 3
        self.state = 'FIRST'
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.angle = None
        self.angle_deg = 0
        self.powerbar = None
        self.powerbar_power = 0

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())
        pass
