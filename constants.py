from math import *
import pygame as pg
DISP_W = 900
DISP_H = 700
BOTTOM_CENTER = (450,700)
CAPTION = 'Bubble Trouble but worse'

#create display
display = pg.display.set_mode((DISP_W,DISP_H))
display_rect = display.get_rect()
pg.display.set_caption(CAPTION)

# colours
BLACK = (0, 0, 0 )
LIGHT_GRAY = (122, 122, 122)
DARK_GRAY = (60,60,60)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
#INDIGO = (111 ,0 ,255)
VIOLET = (127, 0, 255)
#Ball colours
BALL_COLOURS = [RED,ORANGE,YELLOW,GREEN,BLUE,VIOLET]
BG_COLOUR = LIGHT_GRAY
#Game environment constants
WALL_WIDTH = 120
ROOM_WIDTH = DISP_W-2*WALL_WIDTH
WALL_BOUND_L = WALL_WIDTH
WALL_BOUND_R = DISP_W - WALL_WIDTH
WALL_RECT_L = pg.Rect(0,0,WALL_WIDTH,DISP_H)
WALL_RECT_R = pg.Rect(WALL_BOUND_R,0,WALL_WIDTH,DISP_H)

ARROW_BASE = (int(DISP_W/2),DISP_H)
ARROW_LENGTH = 80

ANGLE_MAX = 7*pi/8
ANGLE_MIN = pi/8

#Moving Bubble Constants
BUBBLE_VEL = 10
BUBBLE_DIAMETER = 15
PREBULLET_POS_Y = ARROW_BASE[1]-BUBBLE_DIAMETER

#Grid Constants
GRID_COLS = 20
#rows const?
GRID_ROWS = 10