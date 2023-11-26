from pico2d import *
import game_framework
import Screen.menu_screen
import game_world
from Class.player_Hammer import HammerPlayer


def init():
    global image
    global text
    global player

    running = True
    # image = load_image('./resources/title.png')
    text = load_font("./resources/ENCR10B.TTF", 16)

    player = HammerPlayer()
    game_world.add_object(player, 1)


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
    # text.draw(400, 300, "Hammer Screen", (255, 255, 0))
    game_world.render()
    update_canvas()
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_mode()
        else:
            player.handle_event(event)


def pause():
    pass


def resume():
    pass
