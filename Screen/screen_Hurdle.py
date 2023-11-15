from pico2d import *
import game_framework
import game_world
import Screen.menu_screen

from Class.player_Hurdle import HurdlePlayer
from Class.hurdle import Hurdle


def init():
    global image
    global text
    global player
    global hurdle

    running = True
    image = load_image('./resources/Hurdle/hurdle_Background.png')
    text = load_font("./resources/ENCR10B.TTF", 16)

    player = HurdlePlayer()
    game_world.add_object(player, 1)

    hurdle = Hurdle()
    game_world.add_object(hurdle, 1)

    game_world.add_collision_pair('player:hurdle', player, None)
    game_world.add_collision_pair('player:hurdle', None, hurdle)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()

    game_world.handle_collisions()
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
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
