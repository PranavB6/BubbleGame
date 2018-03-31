import default, time, random, pygame
pygame.init()

#create display
Display = pygame.display.set_mode((default.display_w , default.display_h)) 

# Change title of window
pygame.display.set_caption(default.caption) 

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