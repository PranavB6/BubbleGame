import time, random
import pygame as pg
from math import *
from constants import *
from bubble import *

class game():
	def __init__(self):
		self.over = False

class gameGrid():
	def __init__(self):
		self.rows = GRID_ROWS
		self.cols = GRID_COLS
		self.grid = [[0 for x in range(GRID_COLS)] for y in range(GRID_ROWS)]
		for i in range(GRID_ROWS):
			for j in range(GRID_COLS):
				self.grid[i][j] = gridBubble(GREEN,i,j,True)
				self.grid[i][j].draw()
		self.appendBottom()
		#self.graph = self.makeGraph()
	def draw(self):
		for i in range(self.rows):
			for j in range(GRID_COLS):
				if self.grid[i][j]:
					self.grid[i][j].draw()
	def check(self,bullet_pos,bullet):
		for i in range(self.rows):
			for j in range(GRID_COLS):
				# print(str(i)+","+str(j))
				gridElement = self.grid[i][j]
				if gridElement:
					if gridElement.exists:
						dx = gridElement.pos[0] - bullet_pos[0]
						dy = gridElement.pos[1] - bullet_pos[1]
						combRadius = BUBBLE_RADIUS * 2
						# print(str((int(dx)**2)+(int(dy)**2)))
						# print("DD")
						# print(str(int(dx)^2))
						# if intersecting
						if((int(dx)**2)+(int(dy)**2)<int(combRadius)**2):
							#self.grid[i][j].color = RED
							bullet.getGridPos(self)
						else:
							pass
		#Check if the bottom row is completely null, if not, add a null row
		for j in range(GRID_COLS):
			if self.grid[self.rows-1][j].exists:
				self.appendBottom()

	def checkGameOver(self,game):
		if self.rows == 20:
			game.over == True
			#self.grid[i][j].color = WHITE
	def appendBottom(self):
		row = []
		for j in range(GRID_COLS):
			row.append(gridBubble(BLACK,self.rows,j,False))
		self.grid.append(row)	
		self.rows += 1

def drawBackground():
	display.fill(BG_COLOUR)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)

def drawArrow(arrow_angle):
	#print(arrow_angle)
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