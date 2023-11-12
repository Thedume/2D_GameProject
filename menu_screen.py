from pico2d import *
import game_framework
import title_screen
import screen_HammerThrow
import screen_JavelinThrow
import screen_Hurdle


def init():
    # global background
    global toHammer
    global toJavelin
    global toHurdle

    running = True
    # background = load_image('./resources/tuk_credit.png')
    toHammer = load_image('./resources/throwHammerIcon.png')
    toJavelin = load_image('./resources/javelinThrowIcon.png')
    toHurdle = load_image('./resources/hurdleIcon.png')


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    # background.draw(400, 300)
    # 400, 450
    toHurdle.draw(400, 450)
    # 200, 150
    toHammer.draw(200, 150)
    # 600, 150
    toJavelin.draw(600, 150)
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
                game_framework.push_mode(HammerThrow_screen)
            if pow(75, 2) > (pow(600 - event.x, 2) + pow(450 - event.y, 2)):
                print("In toJavelin Circle")
                game_framework.push_mode(JavelinThrow_screen)
            if pow(75, 2) > (pow(400 - event.x, 2) + pow(150 - event.y, 2)):
                print("In toHurdle Circle")
                game_framework.push_mode(Hurdle_screen)


def pause():
    pass


def resume():
    pass