import time, random
import pygame as pg
from constants import *
pygame.init()

#create display
display = pygame.display.set_mode((DISP_W,DISP_H))

# Change title of window
pygame.display.set_caption(CAPTION)

# Game specific clock
clock = pygame.time.Clock()

def drawBackground():
	display.fill(LIGHT_GRAY)
	#pygame.draw.rect(display,BLACK,10)
	#pygame.draw.rect()
def main():
	print('program start')
	while True:
		drawBackground()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pygame.display.update()
		
		clock.tick(60)



	return


if __name__ == '__main__':
	main()
