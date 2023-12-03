from pico2d import *

import game_world
import server
from Class.angle import Angle
from Class.hammer import Hammer
from Class.power_bar import Powerbar

import game_framework

# self Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 3.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# self Action Speed
TIME_PER_ACTION = 0.85
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

        hammerPlayer.info_message = load_font("./resources/Giants-Inline.TTF", 32)

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
        hammerPlayer.info_message.draw(200, 375, "Press 'Space' to Start", (0, 0, 0))


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
        if not (0 <= hammerPlayer.angle_deg <= 15 or 345 <= hammerPlayer.angle_deg <= 359):
            print(hammerPlayer.angle_deg)
            hammerPlayer.state_machine.handle_event(('FOUL', 0))
        else:
            hammerPlayer.powerbar = Powerbar(hammerPlayer.x + 100, hammerPlayer.y + 5, 2)
            game_world.add_object(hammerPlayer.powerbar, 2)
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        if space_down(e):
            hammerPlayer.angle.isRotate = False
            hammerPlayer.powerbar_power = hammerPlayer.powerbar.power
            print(hammerPlayer.powerbar_power)
        if hammerPlayer.angle:
            game_world.remove_object(hammerPlayer.angle)
        if hammerPlayer.powerbar:
            game_world.remove_object(hammerPlayer.powerbar)

    @staticmethod
    def do(hammerPlayer):
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

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
        hammerPlayer.foul_message = load_font("./resources/Giants-Inline.TTF", 32)
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
        hammerPlayer.foul_message.draw(200, 300, "FOUL!!" + "\n" + "Press 'Space' to Restart", (255, 255, 0))


class StateMachine:
    def __init__(self, hammerPlayer):
        # print("StateMachine __init__")
        self.hammerPlayer = hammerPlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {space_down: Rotate},
            Rotate: {space_down: CheckAngle, foul: Foul},
            CheckAngle: {foul: Foul, space_down: CheckPower},
            CheckPower: {foul: Foul, space_down: Stop},
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
        self.state = 'Idle'
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

    def throw_hammer(self, x, y,a, p):
        server.hammer = Hammer(x, y, a, p)
        game_world.add_object(server.hammer)

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        pass
