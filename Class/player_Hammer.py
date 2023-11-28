from pico2d import *

import game_world
from Class.angle import Angle
from Class.power_bar import Powerbar

import game_framework

# self Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 3.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# self Action Speed
TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

animation_names = {'Idle': 6, 'Rotate': 9, 'Stop': 1}


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def time_out(e):
    return e[0] == 'TIME_OUT'


def foul(e):
    return e[0] == 'FOUL'


class Idle:
    @staticmethod
    def enter(hammerPlayer, e):
        global FRAMES_PER_ACTION
        hammerPlayer.x, hammerPlayer.y = 10, 380  # default : 10, 380
        hammerPlayer.frame = 0
        hammerPlayer.dir = 0
        hammerPlayer.frame = 0
        hammerPlayer.frame_time = 0.0
        hammerPlayer.wait_time = get_time()

        FRAMES_PER_ACTION = animation_names['Idle']
        hammerPlayer.state = 'Idle'
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 30, 30)


class Rotate:
    @staticmethod
    def enter(hammerPlayer, e):
        global FRAMES_PER_ACTION
        print('Enter Rotate')

        hammerPlayer.state = 'Rotate'
        FRAMES_PER_ACTION = animation_names['Rotate']
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        if space_down(e):
            # hammerPlayer.showAngle()
            pass
        pass

    @staticmethod
    def do(hammerPlayer):
        hammerPlayer.x += RUN_SPEED_PPS * game_framework.frame_time
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if hammerPlayer.x >= 160:
            # print("over")
            hammerPlayer.state_machine.handle_event(('FOUL', 0))

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 55, 55)


class CheckAngle:
    @staticmethod
    def enter(hammerPlayer, e):
        print('Enter Angle')
        hammerPlayer.angle = Angle(hammerPlayer.x + 50, hammerPlayer.y + 5)
        game_world.add_object(hammerPlayer.angle, 2)
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        if space_down(e):
            hammerPlayer.angle.isRotate = False
            hammerPlayer.angle_deg = hammerPlayer.angle.deg
            pass
        pass

    @staticmethod
    def do(hammerPlayer):
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 55, 55)


class CheckPower:
    @staticmethod
    def enter(hammerPlayer, e):
        print('Enter Power')
        hammerPlayer.p_dir = 1
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        game_world.remove_object(hammerPlayer.angle)
        game_world.remove_object(hammerPlayer.powerbar)

    @staticmethod
    def do(hammerPlayer):
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if hammerPlayer.p >= 50 or hammerPlayer.p <= 2:
            hammerPlayer.p_dir *= -1
        hammerPlayer.p += hammerPlayer.p_dir * 0.5

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 55, 55)


class Stop:
    @staticmethod
    def enter(hammerPlayer, e):
        print('Enter Stop')
        hammerPlayer.state = 'Stop'
        hammerPlayer.frame = 0

        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        pass

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][hammerPlayer.frame].draw(hammerPlayer.x, hammerPlayer.y, 55, 55)


class Foul:
    @staticmethod
    def enter(hammerPlayer, e):
        print('Enter Foul')
        hammerPlayer.state = 'Stop'
        hammerPlayer.frame = 0
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        pass

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 55, 55)


class StateMachine:
    def __init__(self, hammerPlayer):
        # print("StateMachine __init__")
        self.hammerPlayer = hammerPlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {space_down: Rotate},
            Rotate: {space_down: CheckAngle, foul: Foul},
            CheckAngle: {space_down: CheckPower},
            CheckPower: {space_down: Stop},
            Stop: {},
            Foul: {space_down: Idle}
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
    images = None

    def load_images(self):
        if HammerPlayer.images == None:
            HammerPlayer.images = {}
            for name in animation_names.keys():
                HammerPlayer.images[name] = [load_image("./resources/hammer/player/" + name + "(%d)" % i + ".png") for i in range(1, animation_names[name] + 1)]
            HammerPlayer.font = load_font('./resources/ENCR10B.TTF', 40)
            # HammerPlayer.marker_image = load_image('hand_arrow.png')

    def __init__(self):
        self.x, self.y = 10, 380 # default : 10, 380
        self.frame = 0
        self.load_images()
        self.frame_time = 0.0
        self.p = 0
        self.state = 'Idle'
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.angle = None
        self.angle_deg = 0
        self.powerbar = Powerbar(self.x + 70, self.y + 5, self.p)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())
        pass

    def showAngle(self):
        global angle

        angle = Angle(self.x + 50, self.y + 5)
        game_world.add_object(angle)

    def showPowerbar(self):
        global powerBar

        powerBar = Powerbar(self.x + 40, self.y + 5, self.p)
        game_world.add_object(powerBar)

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        pass
