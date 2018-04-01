import time, random
import pygame as pg
from math import *
from constants import *
pg.init()

#create display
display = pg.display.set_mode((DISP_W,DISP_H))

# Change title of window
pg.display.set_caption(CAPTION)

# Game specific clock
clock = pg.time.Clock()

def drawBackground():
	display.fill(LIGHT_GRAY)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)
	#pg.draw.rect(display,DARK_GRAY,DEMO_RECT)


def drawArrow(arrow_angle):
	arrow_head = calcArrowHead(arrow_angle)
	pg.draw.line(display,BLACK,ARROW_BASE,arrow_head)

def calcArrowHead(arrow_angle):
	x = int(cos(arrow_angle)*ARROW_LENGTH)
	y = int(sin(arrow_angle)*ARROW_LENGTH)
	x = ARROW_BASE[0] + x
	y = ARROW_BASE[1] - y
	return (x,y)

#TODO DEFINE ANGLE LIMITS
def calcMouseAngle(mouse_pos):
	width = mouse_pos[0] - ARROW_BASE[0]
	height = (ARROW_BASE[1] - mouse_pos[1])
	angle = atan2(height,width)
	return angle

def main():
	print('program start')
	mouse_angle = pi/2
	while True:
		drawBackground()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()
				mouse_angle = calcMouseAngle(mouse_pos)
		drawArrow(mouse_angle)
		#drawArrow(pi/4)

		pg.display.update()
		
		clock.tick(60)



	return


if __name__ == '__main__':
	main()
