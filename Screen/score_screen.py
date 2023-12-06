from pico2d import *

import game_framework
import game_world
import server
import Screen.screen_JavelinThrow
# import pannel

from Class.score import Score


# Game object class here


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_SPACE:
                    if server.player.state == 'FIRST':
                        server.player.state = 'SECOND'
                    elif server.player.state == 'SECOND':
                        server.player.state = 'END'

                    game_framework.pop_mode()


def init():
    global score

    score = Score()
    game_world.add_object(score, 3)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.remove_object(score)


def pause():
    pass


def resume():
    pass