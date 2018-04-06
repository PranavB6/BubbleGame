from constants import *
import math, random
import pygame as pg
pg.init()


class bubble():
	def __init__(self, pos, color = None):

		if not color: self.color = BALL_COLOURS[random.randint(0, len(BALL_COLOURS) - 1)]
		else: self.color = color

		self.diameter = BUBBLE_DIAMETER
		self.pos = pos

	def draw(self):
		pg.draw.circle(display, self.color, self.pos, self.diameter)

class bullet(bubble):
	def __init__(self, color , pos , angle):
		bubble.__init__(self, pos, color)
		self.x_vel = cos(angle) * BUBBLE_VEL
		self.y_vel = sin(angle) * BUBBLE_VEL
		self.out_of_bounds = False

	def updatePos(self):
		if self.pos[0]-BUBBLE_DIAMETER <= WALL_BOUND_L:
			self.x_vel = self.x_vel * -1
		elif self.pos[0]+BUBBLE_DIAMETER >= WALL_BOUND_R:
			self.x_vel = self.x_vel * -1
		# print("X: "+str(self.x_vel))
		# print("Y: "+str(self.y_vel))
		# print("POS"+(str(self.pos)))
		x_pos = self.pos[0]
		y_pos = self.pos[1]
		x_pos += self.x_vel
		y_pos -= self.y_vel
		self.pos = (int(round(x_pos)),int(round(y_pos)))

		if self.pos[1]-BUBBLE_DIAMETER <= 0:
			self.out_of_bounds = True
		else:
			self.out_of_bounds = False
		self.draw()

class gridBubble(bubble):
	def __init__(self, row, col, color = None):		

		self.row = row
		self.col = col
		self.alive = True
		self.calcPos()

		bubble.__init__(self, self.pos, color)		

	def calcPos(self):
		# x = BUBBLE_DIAMETER + self.col*BUBBLE_DIAMETER*2+WALL_BOUND_L
		# y = BUBBLE_DIAMETER + self.row*BUBBLE_DIAMETER*2
		x = (self.col * ((ROOM_WIDTH-BUBBLE_DIAMETER) / (GRID_COLS)))+WALL_BOUND_L+BUBBLE_DIAMETER
		if self.row%2 == 0:
			x+=BUBBLE_DIAMETER
		#y = random.randrange(0,DISP_H)
		y = BUBBLE_DIAMETER + self.row*BUBBLE_DIAMETER*2
		self.pos = (int(x),int(y))
		#print(x,y)


