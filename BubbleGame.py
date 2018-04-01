import time, random, pygame
from constants import *
pygame.init()

#create display
Display = pygame.display.set_mode((DISP_W,DISP_H))

# Change title of window
pygame.display.set_caption(CAPTION)

# Game specific clock
clock = pygame.time.Clock()


def main():
	print('program start')
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pygame.display.update()
		clock.tick(60)


	return


if __name__ == '__main__':
	main()
