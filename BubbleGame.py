import time, random
import pygame as pg
pg.init()
from constants import *

import math

#create display
display = pg.display.set_mode((DISP_W,DISP_H))
display_rect = display.get_rect()

# Change title of window
pg.display.set_caption(CAPTION)

# Game specific clock
clock = pg.time.Clock()

def drawBackground():
	display.fill(WHITESMOKE)
	pg.draw.rect(display,DARK_GRAY, WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY, WALL_RECT_R)

def getGun():

	# Load image
	gun = pg.image.load('gun.png').convert_alpha()

	# Get width and height
	gun_rect = gun.get_rect()
	gun_w = gun_rect[2]
	gun_h = gun_rect[3]

	# Scale image
	sf = 0.25
	gun = pg.transform.scale(gun, (int(gun_w * sf), int(gun_h * sf)))

	# Scale Image
	return gun


def putGunInBox(gun):

	# Get gun dimensions
	gun_rect = gun.get_rect()
	gun_w = gun_rect[2]
	gun_h = gun_rect[3]

	# Make a box to put gun in
	# Surface((width, height), flags=0, depth=0, masks=None) -> Surface
	gun_box = pg.Surface((gun_w, gun_h*2))
	gun_box.fill(WHITESMOKE)

	# Put gun in box
	gun_box.blit(gun, gun_rect)

	return gun_box


def main():

	print('program start')

	# ------------------------------
	gun = getGun()
	gun_box = putGunInBox(gun)
	angle = 0
	# ---------------------

	while True:

		drawBackground()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

		angle += 1
		
		# Note: Don't change the original image, you will slowly lose information
		# Rotate the box
		rotated_box = pg.transform.rotate(gun_box, angle)

		# Display the box on the screen
		# Note: center is the pivot point
		display.blit(rotated_box, rotated_box.get_rect( center = display_rect.center))

		pg.display.update()
		
		clock.tick(60)



	return


if __name__ == '__main__': main()
