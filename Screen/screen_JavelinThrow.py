from pico2d import *
import game_framework
import Screen.menu_screen
import game_world
import server
from Class.player_Javelin import JavelinPlayer
from Class.background_javelin import FixedBackground as Background

player_num = {1: 'first', 2: 'second'}

def init():
    server.game = 'hurdle'

    server.f_player_score[server.game] = [None for i in range(3)]
    server.s_player_score[server.game] = [None for i in range(3)]

    server.background_j = Background()
    game_world.add_object(server.background_j, 0)

    server.player = JavelinPlayer()
    game_world.add_object(server.player, 1)


def finish():
    server.player = None
    server.background_j = None
    server.javelin = None
    server.f_player_score = {'hurdle': [None], 'hammer': [None], 'javelin': [None]}
    server.s_player_score = {'hurdle': [None], 'hammer': [None], 'javelin': [None]}
    game_world.clear()
    pass


def update():
    game_world.update()

    game_world.handle_collisions()
    pass


def draw():
    clear_canvas()
    # image.draw(400, 300)

    game_world.render()
    update_canvas()
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_mode(Screen.menu_screen)
        else:
            server.player.handle_event(event)


def pause():
    pass


def resume():
    pass
