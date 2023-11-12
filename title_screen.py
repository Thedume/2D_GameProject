from pico2d import *
import game_framework
import menu_screen


def init():
    global image
    global titleText
    global text

    running = True
    image = load_image('./resources/menuBackground.png')
    titleText = load_font("./resources/Giants-Inline.TTF", 70)
    text = load_font("./resources/Giants-Regular.TTF", 40)


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    titleText.draw(200, 400, "육상 3종 경기", (0, 0, 0))
    text.draw(190, 110, "Press Space to Start!", (0, 0, 0))
    update_canvas()
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(menu_screen)


def pause():
    pass


def resume():
    pass