from pico2d import *
import game_framework
import Screen.title_screen


def init():
    global image
    global logo_start_time

    logo_start_time = get_time()

    running = True
    image = load_image('./resources/tuk_credit.png')


def finish():
    pass


def update():
    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(Screen.title_screen)


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass


def handle_events():
    pass


def pause():
    pass


def resume():
    pass