from pico2d import open_canvas, delay, close_canvas

import game_framework
import Screen.menu_screen as start_mode
# import screen_Hurdle as start_mode
#  title_screen as start_mode
# import menu_screen as start_mode

open_canvas()
game_framework.run(start_mode)
close_canvas()