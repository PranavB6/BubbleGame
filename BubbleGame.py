

import time, random
import pygame as pg
from math import *
from constants import *
from bubble_file import *
from shooter_file import *
from grid_file import *
pg.init()


# Game specific clock
clock = pg.time.Clock()


def drawBackground():
	display.fill(BG_COLOUR)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)


def main():
	print('program start')
	mouse_pos = (0,0)

	# ----------------------------

	gun = Shooter(pos = BOTTOM_CENTER)
	gun.putInBox()
	gamegrid = gameGrid()

	# ----------------------------	

	while True:
		drawBackground()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()

			if event.type == pg.MOUSEBUTTONDOWN:
				# gamegrid.check(mouse_pos)
				gun.fire()

			#Ctrl+C to quit
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.quit()
					quit()


		gamegrid.draw()

		gun.rotate(mouse_pos)
		gun.draw_bullet()


		pg.display.update()
		clock.tick(60)


	return

if __name__ == '__main__': main()
