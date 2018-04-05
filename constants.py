import pygame as pg
from math import pi
DISP_W = 900
DISP_H = 700
BOTTOM_CENTER = (450,700)
CAPTION = 'Bubble Trouble but worse'

# colours
BLACK = (0, 0, 0 )
LIGHT_GRAY = (122, 122, 122)
DARK_GRAY = (60,60,60)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
WHITESMOKE = (245,245,245)
BG_COLOUR = WHITESMOKE

#Game environment constants
WALL_WIDTH = 120
WALL_BOUND_L = WALL_WIDTH
WALL_BOUND_R = DISP_W - WALL_WIDTH
WALL_RECT_L = pg.Rect(0,0,WALL_WIDTH,DISP_H)
WALL_RECT_R = pg.Rect(WALL_BOUND_R,0,WALL_WIDTH,DISP_H)



#create display
display = pg.display.set_mode((DISP_W,DISP_H))
display_rect = display.get_rect()


ANGLE_MAX = 180 - 15
ANGLE_MIN = 0 + 15