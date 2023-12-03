from pico2d import *
import game_framework
import Screen.menu_screen
import game_world
import server
from Class.player_Hammer import HammerPlayer
from Class.background_hammer import FixedBackground as Background


def init():
    global foul_message
    #
    foul_message = load_font("./resources/Giants-Inline.TTF", 65)

    server.background_h = Background()
    game_world.add_object(server.background_h, 0)

    server.player = HammerPlayer()
    game_world.add_object(server.player, 1)



def finish():
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
