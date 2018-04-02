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

def getImg():
	gun_og = pg.image.load('gun.png').convert()
	gun_og_rect = gun_og.get_rect()

	gun_og_rect_w = gun_og_rect[2]
	gun_og_rect_h = gun_og_rect[3]


	sf = 0.25
	gun_og = pg.transform.scale(gun_og, (int(gun_og_rect_w * sf), int(gun_og_rect_h * sf)))

	return gun_og

def main():

	print('program start')

	# ------------------------------


	image_og = getImg()
	image_og_rect = image_og.get_rect( center = display_rect.center) # center = (display_rect.center)
	angle = 0

	# ---------------------

	while True:
		drawBackground()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

		angle += 1
		gun = pg.transform.rotate(image_og, angle)
		gun_rect = gun.get_rect( center = (450,650))

		display.blit(gun, gun_rect)
		pg.display.update()
		
		clock.tick(60)



	return


if __name__ == '__main__':
	main()
