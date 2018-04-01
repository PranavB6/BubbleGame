import time, random
import pygame as pg
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
def main():
	print('program start')
	while True:
		drawBackground()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

		pg.display.update()
		
		clock.tick(60)



	return


if __name__ == '__main__':
	main()
