from constants import *
import math, random
import pygame as pg
pg.init()


class bubble():
	def __init__(self, pos, color = None):

		if not color: self.color = BALL_COLOURS[random.randint(0, len(BALL_COLOURS) - 1)]
		else: self.color = color

		self.radius = BUBBLE_RADIUS
		self.pos = pos

	def draw(self):
		pg.draw.circle(display, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class bullet(bubble):
	def __init__(self, color , pos , angle):
		bubble.__init__(self, pos, color)
		self.x_vel = cos(angle) * BUBBLE_VEL
		self.y_vel = sin(angle) * BUBBLE_VEL
		self.out_of_bounds = False

	def updatePos(self):
		if self.pos[0]-BUBBLE_RADIUS <= WALL_BOUND_L:
			self.x_vel = self.x_vel * -1
		elif self.pos[0]+BUBBLE_RADIUS >= WALL_BOUND_R:
			self.x_vel = self.x_vel * -1
		# print("X: "+str(self.x_vel))
		# print("Y: "+str(self.y_vel))
		# print("POS"+(str(self.pos)))
		x_pos = self.pos[0]
		y_pos = self.pos[1]
		x_pos += self.x_vel
		y_pos -= self.y_vel
		self.pos = (x_pos, y_pos)

		if self.pos[1]-BUBBLE_RADIUS <= 0:
			self.out_of_bounds = True
		else:
			self.out_of_bounds = False
		self.draw()

class gridBubble(bubble):
	def __init__(self, row, col, exists, color = None):		

		self.row = row
		self.col = col
		self.alive = True
		self.calcPos()
		self.exists = exists

		bubble.__init__(self, self.pos, color)		

	def calcPos(self):
		# x = BUBBLE_RADIUS + self.col*BUBBLE_RADIUS*2+WALL_BOUND_L
		# y = BUBBLE_RADIUS + self.row*BUBBLE_RADIUS*2
		x = (self.col * ((ROOM_WIDTH-BUBBLE_RADIUS) / (GRID_COLS)))+WALL_BOUND_L+BUBBLE_RADIUS
		if self.row%2 == 0:
			x+=BUBBLE_RADIUS
		#y = random.randrange(0,DISP_H)
		y = BUBBLE_RADIUS + self.row*BUBBLE_RADIUS*2
		self.pos = (int(x),int(y))
		#print(x,y)


