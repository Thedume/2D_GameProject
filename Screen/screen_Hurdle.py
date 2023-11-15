from pico2d import *
import game_framework
import game_world
import Screen.menu_screen

from Class.player_Hurdle import HurdlePlayer
from Class.grass import Grass
from Class.hurdle import Hurdle


def init():
    global image
    global text
    global player
    global grass
    global hurdle

    running = True
    # image = load_image('./resources/title.png')
    text = load_font("./resources/ENCR10B.TTF", 16)

    grass = Grass()
    game_world.add_object(grass, 0)

    player = HurdlePlayer()
    game_world.add_object(player, 1)

    hurdle = [Hurdle() for _ in range(10)]
    game_world.add_objects(hurdle, 1)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()

    # game_world.handle_collisions()
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
