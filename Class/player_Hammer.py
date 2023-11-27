from pico2d import *

import game_framework

# self Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# self Action Speed
TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

animation_names = {'Idle': 6, 'Rotate': 9}


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(hammerPlayer, e):
        global FRAMES_PER_ACTION
        hammerPlayer.dir = 0
        hammerPlayer.frame = 0
        hammerPlayer.wait_time = get_time()

        FRAMES_PER_ACTION = animation_names['Idle']
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        # hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 75, 75)


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
        pass

    @staticmethod
    def do(hammerPlayer):
        # hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 100, 100)


class Power:
    @staticmethod
    def enter(hammerPlayer, e):
        print('Enter Power')
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        # hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 100, 100)


class Stop:
    @staticmethod
    def enter(hammerPlayer, e):
        print('Enter Stop')
        pass

    @staticmethod
    def exit(hammerPlayer, e):
        pass

    @staticmethod
    def do(hammerPlayer):
        # hammerPlayer.frame = (hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        hammerPlayer.frame = ( hammerPlayer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(hammerPlayer):
        hammerPlayer.images[hammerPlayer.state][int(hammerPlayer.frame)].draw(hammerPlayer.x, hammerPlayer.y, 100, 100)


class StateMachine:
    def __init__(self, hammerPlayer):
        # print("StateMachine __init__")
        self.hammerPlayer = hammerPlayer
        self.cur_state = Idle

        self.transitions = {
            Idle: {space_down: Rotate},
            Rotate: {space_down: Power},
            Power: {space_down: Stop}
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
        self.x, self.y = 120, 150
        self.frame = 0
        self.load_images()
        self.frame_time = 0.0
        self.state = 'Idle'
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        pass