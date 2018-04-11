from constants import *
import math, random
from bubble import *
import pygame as pg
pg.init()


class Shooter():

	def __init__(self, image = 'cannon.png', pos = display_rect.center):

		# center position of the image
		self.pos = pos
		self.pos_x, self.pos_y = pos[0], pos[1]

		# Load image
		self.shooter = pg.image.load(image).convert_alpha()

		# Get width and height
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w = self.shooter_rect[2]
		self.shooter_h = self.shooter_rect[3]

		# Scale image
		sf = 00.20
		self.shooter = pg.transform.scale(self.shooter, (int(self.shooter_w * sf), int(self.shooter_h * sf)))

		# Get new width and height
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w = self.shooter_rect[2]
		self.shooter_h = self.shooter_rect[3]


		self.loaded = bubble(random.choice(BALL_COLOURS), self.pos)
		self.fired = None
		self.angle = 90

		return

	# I could have put this in the initialization but I wanted to emphasize the fact that the image we are actually rotating is in a box
	def putInBox(self):

		# Make a box to put shooter in
		# Surface((width, height), flags=0, depth=0, masks=None) -> Surface
		self.shooter_box = pg.Surface((self.shooter_w, self.shooter_h*2),pg.SRCALPHA,32)
		self.shooter_box.fill((0,0,0,0))

		# Put shooter in box
		self.shooter_box.blit(self.shooter, (0,0))

		# Since we want 90 to be when the shooter is pointing straight up, we rotate it
		self.shooter_box = pg.transform.rotate(self.shooter_box, -90)

	# Cuz why not
	def draw(self):
		display.blit(self.shooter_box, self.pos)

	def draw_line(self):

		length = 200

		# line(Surface, color, start_pos, end_pos, width=1) -> Rect
		end = ( (math.cos(math.radians(self.angle)) * length) + display_rect[2]/2, display_rect[3] - (math.sin(math.radians(self.angle)) * length))
		
		pg.draw.line(display, RED , self.pos, end, 1)

		return

	# Rotates an image and displays it
	def rotate(self, mouse_pos):
		# Get angle of rotation (in degrees)
		self.angle = self.calcMouseAngle(mouse_pos)

		# Get a rotated version of the box to display. Note: don't keep rotating the original as that skews the image
		rotated_box = pg.transform.rotate(self.shooter_box, self.angle)

		self.draw_line()

		# display the image
		display.blit(rotated_box, rotated_box.get_rect( center = self.pos))


		return

	def calcMouseAngle(self, mouse_pos):
		# Get mouse position and decompose it into x and y
		mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

		# Do some quick maths and get the angle
		width = mouse_x - self.pos_x
		height = self.pos_y - mouse_y
		angle = math.atan2(height,width)
		degrees = math.degrees(angle)		# convert to degrees

		# Restrict the angles, we don't want the user to be able to point all the way
		return max(min( degrees , ANGLE_MAX), ANGLE_MIN)


	def draw_bullet(self,game):
		if self.fired:
			if self.fired.out_of_bounds or game.over:
				self.fired = None
				#KEEP THIS RETURN STATEMENT. IDK WHY BUT ITS STOPPING A BUG I THINK
				return
		#Updates after checking if out of bounds to prevent drawing a bullet when it
		#doesnt exist.
		if self.fired:
			self.fired.updatePos()
		self.loaded.draw()
		return

	def fire(self):

		rads = math.radians(self.angle)
		if self.fired is None:
			self.fired = bullet( self.loaded.color, self.pos, rads )
			self.loaded = bubble(random.choice(BALL_COLOURS),(self.pos))
		return
