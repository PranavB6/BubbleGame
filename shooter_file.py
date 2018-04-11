from constants import *
import math, random
from bubble import *
import pygame as pg
pg.init()


class Shooter():

	def __init__(self, image = 'cannon.png', pos = display_rect.center):

		# get center position of the image
		self.pos = pos
		self.pos_x, self.pos_y = pos[0], pos[1]

		# Load image and get its width and height
		self.shooter = pg.image.load(image).convert_alpha()
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w, self.shooter_h = self.shooter_rect[2], self.shooter_rect[3]

		# Scale image
		sf = 00.20
		self.shooter = pg.transform.scale(self.shooter, (int(self.shooter_w * sf), int(self.shooter_h * sf)))

		# Get new width and height of image
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w, self.shooter_h = self.shooter_rect[2], self.shooter_rect[3]

		# Setup position of 'reloads'
		self.reload1_pos = (self.pos[0] + 6.5*BUBBLE_RADIUS, self.pos[1] - 20)
		self.reload2_pos = (self.pos[0] + 8.5*BUBBLE_RADIUS, self.pos[1] - 20)
		self.reload3_pos = (self.pos[0] + 10.5*BUBBLE_RADIUS, self.pos[1] - 20)

		# Initialize the loaded bullet and its reloads 
		self.fired = None
		self.loaded = bubble(random.choice(BALL_COLOURS), self.pos)
		self.reload1 = bubble(random.choice(BALL_COLOURS), self.reload1_pos)
		self.reload2 = bubble(random.choice(BALL_COLOURS), self.reload2_pos)
		self.reload3 = bubble(random.choice(BALL_COLOURS), self.reload3_pos)

		# Initialize angle
		self.angle = 90

		return

	# I could have put this in the initialization but I wanted to emphasize the fact that the image we are actually rotating is in a box
	def putInBox(self):

		# Make a box to put shooter in, make it transparent
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

		# The start position is the position of the shooter, now find the end position
		# line(Surface, color, start_pos, end_pos, width=1) -> Rect
		end = ((math.cos(math.radians(self.angle)) * ARROW_LENGTH) + display_rect[2]/2, 
				display_rect[3] - (math.sin(math.radians(self.angle)) * ARROW_LENGTH))
		
		# draw the line
		pg.draw.line(display, RED, self.pos, end, 1)
		return

	# Rotates an image and displays it
	def rotate(self, mouse_pos):

		# Get angle of rotation (in degrees)
		self.angle = self.calcMouseAngle(mouse_pos)

		# Get a rotated version of the box to display. Note: don't keep rotating the original as that skews the image
		rotated_box = pg.transform.rotate(self.shooter_box, self.angle)

		self.draw_line()

		# blit the 'new' shooter image to the display. Make sure it's center is the shooter's center
		# since rotating it skews its center point
		display.blit(rotated_box, rotated_box.get_rect( center = self.pos))
		return

	def calcMouseAngle(self, mouse_pos):
		# Get mouse position and decompose it into x and y
		mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

		# Do some quick maths and get the angle that the mouse is making relative to the shooter's center
		width = mouse_x - self.pos_x
		height = self.pos_y - mouse_y
		angle = math.atan2(height,width)

		# convert to degrees
		degrees = math.degrees(angle)		

		# Restrict the angles, we don't want the user to be able to point all the way
		return max(min(degrees , ANGLE_MAX), ANGLE_MIN)


	def draw_bullet(self,game):

		# if a bullet has been fired but it's out of bounds or the game is over, destroy it
		if self.fired:
			if self.fired.out_of_bounds or game.over:
				self.fired = None
				# KEEP THIS RETURN STATEMENT. ITS STOPS A BUG
				# return

		# Updates after checking if out of bounds to prevent drawing a bullet when it
		# doesnt exist.
		if self.fired:
			self.fired.updatePos(game)

		self.loaded.draw(game)
		self.reload1.draw(game)
		self.reload2.draw(game)
		self.reload3.draw(game)

		return

	def fire(self):

		# convert to radians to pass to bullet class
		rads = math.radians(self.angle)

		# If a fired bullet is not on the field, fire a new one
		if self.fired is None:
			self.fired = bullet( self.loaded.color, self.pos, rads )
			self.loaded = bubble(self.reload1.color, (self.pos))
			self.reload1 = bubble(self.reload2.color, self.reload1_pos)
			self.reload2 = bubble(self.reload3.color, self.reload2_pos)
			self.reload3 = bubble(random.choice(BALL_COLOURS), self.reload3_pos)
		return
