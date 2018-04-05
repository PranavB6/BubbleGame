import time, random
import pygame as pg
from math import *
from constants import *
from bubble_file import *
from shooter_file import *
# from grid_file import *
pg.init()


# Game specific clock
clock = pg.time.Clock()


def drawBackground():
	display.fill(BG_COLOUR)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)


def main():
	print('program start')

	# ----------------------------

	gun = Shooter(center = BOTTOM_CENTER)
	gun.putInBox()

	# ----------------------------

	mouse_angle = pi/2
	mouse_pos = (0,0)
	gameBullet = None

	preBullet = bubble(BOTTOM_CENTER)
	preBullet.draw()
	# gamegrid = gameGrid()

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
				#TODO: Implement singleton
				if gameBullet:
					pass
				else:pass
					# gameBullet = bullet(preBullet.color,calcArrowHead(mouse_angle),mouse_angle)
					# preBullet = bubble(BALL_COLOURS[random.randint(0,len(BALL_COLOURS)-1)],ARROW_BASE)
					# preBullet.draw()
					# gameBullet.draw()

			#Ctrl+C to quit
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.quit()
					quit()


		if gameBullet:
			gameBullet.updatePos()
			if gameBullet.out_of_bounds:
				gameBullet = None

		preBullet.draw()
		# gamegrid.draw()

		gun.rotate(mouse_pos)
		preBullet.draw()
		pg.display.update()
		clock.tick(60)


	return

if __name__ == '__main__': main()
