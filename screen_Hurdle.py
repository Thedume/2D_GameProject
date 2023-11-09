from pico2d import *
import game_framework
import game_world
import menu_screen
from player_Hurdle import HurdlePlayer
from grass import Grass


def init():
    global image
    global text
    global player
    global grass

    running = True
    # image = load_image('./resources/title.png')
    text = load_font("./resources/ENCR10B.TTF", 16)

    grass = Grass()
    game_world.add_object(grass, 0)

    player = HurdlePlayer()
    game_world.add_object(player, 1)

def finish():
    pass


def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    game_world.render()
    # 스크린 위치 확인용
    # text.draw(400, 300, "Hurdle Screen", (255, 255, 0))
    update_canvas()


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
