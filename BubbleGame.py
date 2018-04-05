import time, random
import pygame as pg
pg.init()
from constants import *
from shooter_file import Shooter
import math



# Change title of window
pg.display.set_caption(CAPTION)

# Game specific clock
clock = pg.time.Clock()

def drawBackground():
	display.fill(WHITESMOKE)
	pg.draw.rect(display,DARK_GRAY, WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY, WALL_RECT_R)







def main():

	print('program start')

	# ------------------------------
	# Initialize the shooter
	gun = Shooter(center = BOTTOM_CENTER)
	# put it in a box
	gun.putInBox()
	
	# ---------------------

	while True:

		drawBackground()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()
				
		# Rotate and draw gun
		gun.rotate(mouse_pos)

		

		# Display the box on the screen
		# Note: center is the pivot point
		

		pg.display.update()
		
		clock.tick(60)



	return


if __name__ == '__main__': main()
