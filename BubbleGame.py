from colours import *
import default, time, random, math, pygame
pygame.init()

#create display
Display = pygame.display.set_mode((default.display_w , default.display_h)) 

# Change title of window
pygame.display.set_caption(default.caption) 

# Game specific clock
clock = pygame.time.Clock()

dirty_rects = []


class Shooter():

	def __init__(self, pos, base_radius = 50, shaft_length = 80, shaft_width = 20):
		self.pos = pos
		self.x, self.y = pos
		self.base_radius = base_radius
		self.shaft_length = shaft_length
		self.shaft_width = shaft_width
		self.tip_x = self.x
		self.tip_y = self.y - self.shaft_length

		# Draw the part that actually shoots
		# aaline(Surface, color, startpos, endpos, blend=1)
		self.shaft_rect = pygame.draw.line(Display, Blue, self.pos, (self.tip_x, self.tip_y), self.shaft_width)

		# Draw the base
		self.draw_base()

	# pygame.draw.circle(screen, color, (x,y), radius, thickness)
	def draw_base(self): pygame.draw.circle(Display, White, self.pos, self.base_radius)

	def erase_shaft(self):
		# rect = [int(x + 5) for x in self.shaft_rect]

		# pygame.draw.rect(Display, Red, self.shaft_rect)
		pass
		
	def update_shaft(self, tip_x):

		# new x value
		self.tip_x = tip_x	

		if (tip_x > (self.x + self.shaft_length)): self.tip_x = self.x + self.shaft_length
		if (tip_x < (self.x - self.shaft_length)): self.tip_x = self.x - self.shaft_length


		self.erase_shaft()

	

		# get new x value from old x value
		temp_x = self.tip_x - default.display_w/2

		print('tip_x', self.tip_x)
		print('temp_x', temp_x)
		print('shaft_length', self.shaft_length)
		temp_y = int( math.sqrt( (self.shaft_length)**2 - (temp_x)**2 ))
		self.tip_y = default.display_h - temp_y


		self.shaft_rect = pygame.draw.line(Display, Blue, self.pos, (self.tip_x, self.tip_y), self.shaft_width)

		self.draw_base()

		return self.tip_x

def main():
	print('program start')
	global dirty_rects

	shooter = Shooter(default.display_bottom_center)
	delta_tip_x = 0
	tip_x = int(default.display_w/2)

	while True:
		Display.fill(White)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					delta_tip_x = 1
				if event.key == pygame.K_RIGHT:
					delta_tip_x = -1

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					delta_tip_x = 0



		tip_x += delta_tip_x
		tip_x = shooter.update_shaft(tip_x)


		

		# Display.blit(circle, (0,0))
		pygame.display.update()
		dirty_rects = [dirty_rects]

		clock.tick(60)


	return


if __name__ == '__main__':
	main()