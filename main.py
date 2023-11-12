from pico2d import open_canvas, delay, close_canvas

import game_framework
# import logo_screen as start_mode
# import screen_Hurdle as start_mode
import title_screen as start_mode
# import menu_screen as start_mode

open_canvas()
game_framework.run(start_mode)
close_canvas()