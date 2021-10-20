from pygame.math import Vector2 as vec

width, height = 610, 670
top_bottom_buffer = 50
maze_width, maze_height = width-top_bottom_buffer, height-top_bottom_buffer
fps = 60
columns = 28
rows = 30

coin_radius = 4

black = (0,0,0)
red = (200, 20, 20)
grey = (107, 107, 107)
white = (255, 255, 255)
yellow = (180, 180, 50)
blue = (40, 80, 200)
player_colour = (190, 190, 60)
green = (0,128,0)


start_text_size = 16
start_font = 'arial_black'

player_start_pos = 0