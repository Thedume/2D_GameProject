from pico2d import *
import math

open_canvas()

# grass = load_image('grass.png')
character = load_image('./resources/hammer/player/3.png')

# grass.draw_now(400, 30)
character.draw_now(400, 90)

x = 400
y = 90

a = 400
b = 90
r = 255

delay(1000)

# while (True):
#     while (x < 800):
#         clear_canvas_now()
#         grass.draw_now(400, 30)
#         character.draw_now(x, y)
#         x = x + 4
#         delay(0.01)
#
#     while (y < 600):
#         clear_canvas_now()
#         grass.draw_now(400, 30)
#         character.draw_now(x, y)
#         y = y + 4
#         delay(0.01)
#
#     while (x > 0):
#         clear_canvas_now()
#         grass.draw_now(400, 30)
#         character.draw_now(x, y)
#         x = x - 4
#         delay(0.01)
#
#     while (y > 90):
#         clear_canvas_now()
#         grass.draw_now(400, 30)
#         character.draw_now(x, y)
#         y = y - 4
#         delay(0.01)
#
#     while (x < 400):
#         clear_canvas_now()
#         grass.draw_now(400, 30)
#         character.draw_now(x, y)
#         x = x + 4
#         delay(0.01)
#
#     for t in range(0, 360):
#         clear_canvas_now()
#         grass.draw_now(400, 30)
#         character.draw_now(a + r * math.sin(math.radians(t)), b + r * math.cos(math.radians(t)) + r)
#
#         delay(0.01)

close_canvas()
