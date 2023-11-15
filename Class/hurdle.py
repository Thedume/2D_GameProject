import random
import math
import game_framework

from pico2d import *

import game_world

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Hurdle:
    images = None

    def load_images(self):
        if Hurdle.images == None:
            print("Load_Image")
            Hurdle.images = load_image("./Resources/Hurdle/hurdle.png")

    def __init__(self):
        self.x, self.y = 700, 100
        self.load_images()
        self.dir = -1
        self.isDown = False
        self.w, self.h = 100, 100

    def update(self):
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x < 0:
            game_world.remove_object(self)
        # self.x = clamp(800, self.x, 1600)
        pass

    def draw(self):
        if not self.isDown:
            Hurdle.images.draw(self.x, self.y, self.w, self.h)

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - (self.w / 2), self.y - (self.h / 2), self.x + (self.w / 2), self.y + (self.h / 2)

    def handle_collision(self, group, other):
        pass

