from constants import *
import math
import pygame as pg
pg.init()


class Shooter():

	def __init__(self, image = 'gun.png', center = display_rect.center):

		# center position of the image
		self.center = center 
		self.center_x, self.center_y = center[0], center[1]

		# Load image
		self.shooter = pg.image.load(image).convert_alpha()

		# Get width and height
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w = self.shooter_rect[2]
		self.shooter_h = self.shooter_rect[3]

		# Scale image
		sf = 00.25
		self.shooter = pg.transform.scale(self.shooter, (int(self.shooter_w * sf), int(self.shooter_h * sf)))

		# Get new width and height
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w = self.shooter_rect[2]
		self.shooter_h = self.shooter_rect[3]

		return

	# I could have put this in the initialization but I wanted to emphasize the fact that the image we are actually rotating is in a box
	def putInBox(self):

		# Make a box to put shooter in
		# Surface((width, height), flags=0, depth=0, masks=None) -> Surface
		self.shooter_box = pg.Surface((self.shooter_w, self.shooter_h*2))
		self.shooter_box.fill(BG_COLOUR)

		# Put shooter in box
		self.shooter_box.blit(self.shooter, (0,0))

		# Since we want 90 to be when the shooter is pointing straight up, we rotate it
		self.shooter_box = pg.transform.rotate(self.shooter_box, -90)

	# Cuz why not
	def draw(self):
		display.blit(self.shooter_box, self.center)

	# Rotates an image and displays it
	def rotate(self, mouse_pos):
		print(mouse_pos, end = ' ')
		# Get angle of rotation (in degrees)
		angle = self.calcMouseAngle(mouse_pos)

		print(angle)

		# Get a rotated version of the box to display. Note: don't keep rotating the original as that skews the image
		rotated_box = pg.transform.rotate(self.shooter_box, angle)

		# display the image
		display.blit(rotated_box, rotated_box.get_rect( center = self.center))

	def calcMouseAngle(self, mouse_pos):
		# Get mouse position and decompose it into x and y
		mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

		# Do some quick maths and get the angle
		width = mouse_x - self.center_x
		height = self.center_y - mouse_y
		angle = math.atan2(height,width)
		degrees = math.degrees(angle)		# convert to degrees

		# Restrict the angles, we don't want the user to be able to point all the way
		return max(min( degrees , ANGLE_MAX), ANGLE_MIN)


class Bullet():

	def __init__(self):



		return
'''
def drawArrow(arrow_angle):
	arrow_head = calcArrowHead(arrow_angle)
	pg.draw.line(display,BLACK,ARROW_BASE,arrow_head)

def calcArrowHead(arrow_angle):
	x = int(cos(arrow_angle)*ARROW_LENGTH)
	y = int(sin(arrow_angle)*ARROW_LENGTH)
	x = ARROW_BASE[0] + x
	y = ARROW_BASE[1] - y
	return (x,y)

def calcMouseAngle(mouse_pos):
	width = mouse_pos[0] - ARROW_BASE[0]
	height = (ARROW_BASE[1] - mouse_pos[1])
	angle = atan2(height,width)
	return max(min(angle,ANGLE_MAX),ANGLE_MIN)
'''