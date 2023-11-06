from pico2d import *
import game_framework
import title_screen
import HammerThrow_screen
import JavelinThrow_screen
import Hurdle_screen


def init():
    # global background
    global toHammer
    #toSpear, toRunning

    running = True
    # background = load_image('./resources/tuk_credit.png')
    toHammer = load_image('./resources/throwHammerIcon.png')
    # toSpear = load_image('')
    # toRunning = load_image('')


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    # background.draw(400, 300)
    # 400, 150
    # toRunning.draw(400, 150)
    # 200, 450
    toHammer.draw(200, 150)
    # 600, 450
    # toSpeer.draw(600, 450)
    update_canvas()
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if pow(75, 2) > (pow(200 - event.x, 2) + pow(450 - event.y, 2)):
                print("In toHammer Circle")
                game_framework.push_mode(hammer_screen)


def pause():
    pass


def resume():
    pass