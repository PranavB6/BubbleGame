from math import *
import pygame as pg

DISP_W = 900
DISP_H = 700
BOTTOM_CENTER = (450,700)
CAPTION = "Like Bubble Trouble but BETTER"

# create display
display = pg.display.set_mode((DISP_W,DISP_H))
display_rect = display.get_rect()
pg.display.set_caption(CAPTION)

# Ball colours
BLACK = (0, 0, 0 )
MIDDLE_GRAY = (80,80,80)
LIGHT_GRAY = (122, 122, 122)
WHITESMOKE = (150,150,150)
DARK_GRAY = (70,70,70)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
VIOLET = (127, 0, 200)

BALL_COLOURS = [RED,YELLOW,GREEN,BLUE,VIOLET]
BG_COLOUR = None

# Game environment constants
WALL_WIDTH = 120
FLOOR_HEIGHT = 124
ROOM_WIDTH = DISP_W - (2 * WALL_WIDTH)
WALL_BOUND_L = WALL_WIDTH
WALL_BOUND_R = DISP_W - WALL_WIDTH
WALL_BOUND_FLOOR = DISP_H - FLOOR_HEIGHT
WALL_RECT_L = pg.Rect(0, 0, WALL_WIDTH, DISP_H)
WALL_RECT_R = pg.Rect(WALL_BOUND_R, 0, WALL_WIDTH, DISP_H)
WALL_RECT_FLOOR = pg.Rect(0, WALL_BOUND_FLOOR, DISP_W, FLOOR_HEIGHT)

# Shooter's Aimer constants
ARROW_BASE = (int(DISP_W/2),DISP_H)
ARROW_LENGTH = 600

# Min and max degrees that the shooter can rotate in
ANGLE_MAX = 180 - 15
ANGLE_MIN = 0 + 15

# Moving Bubble Constants
BUBBLE_VEL = 12
BUBBLE_RADIUS = 16
PREBULLET_POS_Y = ARROW_BASE[1] - BUBBLE_RADIUS

# Grid Constants
GRID_COLS = 20
GRID_ROWS = 10
GAMEOVER_ROWS = 19
APPEND_COUNTDOWN = 6