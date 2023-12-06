from pico2d import *
import game_framework
import game_world
import Screen.menu_screen
import server

from Class.background_hurdle import FixedBackground as Background
from Class.player_Hurdle import HurdlePlayer
from Class.hurdle import Hurdle


def init():
    server.game = 'hurdle'

    server.f_player_score[server.game] = [None for i in range(1)]
    server.s_player_score[server.game] = [None for i in range(1)]

    server.background_hurdle = Background()
    game_world.add_object(server.background_hurdle, 0)

    server.player = HurdlePlayer()
    game_world.add_object(server.player, 1)


    game_world.add_collision_pair('player:hurdle', server.player, None)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()

    game_world.handle_collisions()
    pass


def draw():
    clear_canvas()
    game_world.render()
    # 스크린 위치 확인용
    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_mode(Screen.menu_screen)
        else:
            server.player.handle_event(event)


def pause():
    # player.wait_time = 10000000000000000000000000000000.0
    pass


def resume():
    # player.wait_time = get_time()
    pass
