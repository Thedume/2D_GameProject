from pico2d import *
import game_framework
import menu_screen
from player import Player


def init():
    global image
    global text
    global player

    running = True
    # image = load_image('./resources/title.png')
    text = load_font("./resources/ENCR10B.TTF", 16)

    player = Player()


def finish():
    pass


def update():
    player.update()
    pass


def draw():
    clear_canvas()
    # image.draw(400, 300)
    text.draw(400, 300, "Hurdle Screen", (255, 255, 0))
    player.draw()
    update_canvas()
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_mode()


def pause():
    pass


def resume():
    pass
