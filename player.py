from pico2d import *

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


class Player:
    def __init__(self):
        self.x, self.y = 50, 90
        self.frame = 0
        self.action = 3
        self.image = load_image("./resources/animation_sheet.png")
        self.font = load_font("./resources/ENCR10B.TTF", 16)
        self.frame_time = 0.0
        # self.state_machine = StateMachine(self)
        # self.state_machine.start()

    def update(self):
        self.frame = (self.frame + 1) % 8
        # self.state_machine.update()

    def handle_event(self, event):
        # self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame) * 100, self.action * 100, 100, 100, self.x, self.y)
        # self.state_machine.draw()
        # self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        pass