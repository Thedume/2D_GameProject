from pico2d import *
import game_framework
import Screen.title_screen
import Screen.screen_HammerThrow
import Screen.screen_JavelinThrow
import Screen.screen_Hurdle
import Screen.hurdleMenu_screen


def init():
    global background
    global toHammer
    global toJavelin
    global toHurdle
    global circle

    running = True
    background = load_image('./resources/menuBackground.png')
    toHammer = load_image('./resources/Hammer/throwHammerIcon.png')
    toJavelin = load_image('./resources/Javelin/javelinThrowIcon.png')
    toHurdle = load_image('./resources/Hurdle/hurdleIcon.png')

    circle = load_image('./resources/Circle.png')


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    background.draw(400, 300)
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
                game_framework.change_mode(Screen.screen_HammerThrow)
            if pow(75, 2) > (pow(600 - event.x, 2) + pow(450 - event.y, 2)):
                print("In toJavelin Circle")
                game_framework.change_mode(Screen.screen_JavelinThrow)
            if pow(75, 2) > (pow(400 - event.x, 2) + pow(150 - event.y, 2)):
                print("In toHurdle Circle")
                game_framework.change_mode(Screen.screen_Hurdle)
                game_framework.push_mode(Screen.hurdleMenu_screen)
        elif event.type == SDL_MOUSEMOTION:
            if pow(75, 2) > (pow(200 - event.x, 2) + pow(450 - event.y, 2)):
                circle.draw(200, 450)
            if pow(75, 2) > (pow(600 - event.x, 2) + pow(450 - event.y, 2)):
                circle.draw(600, 450)
            if pow(75, 2) > (pow(400 - event.x, 2) + pow(150 - event.y, 2)):
                circle.draw(400, 150)


def pause():
    pass


def resume():
    pass