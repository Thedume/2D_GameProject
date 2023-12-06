from pico2d import *
import time

import game_framework
import game_world
import Screen.screen_Hurdle
# import pannel

# from pannel import Pannel


# Game object class here


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_s:
                    countdown()
                    game_framework.pop_mode()


def init():
    global font
    global text

    font = load_font("./resources/Giants-Regular.TTF", 52)
    text = "Press 'S' to Start!"
    # game_world.add_object(font, 3)


def update():
    game_world.update()


def draw():
    clear_canvas()
    font.draw(160, 500, text, (0, 0, 0))
    update_canvas()


def finish():
    pass


def pause():
    pass


def resume():
    pass


def countdown(num_of_secs=3):
    global text
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        text = "{:02d}:{:02d}".format(m, s)
        # font.draw(160, 500, min_sec_format, (0, 0, 0))
        # print(min_sec_format, end="/r")
        time.sleep(1)
        num_of_secs -= 1

