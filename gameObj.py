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
		self._cols = GRID_COLS
		self.grid = [[0 for x in range(self._cols)] for y in range(self.rows)]
		for i in range(self.rows):
			for j in range(self._cols):

				if j % 2:
					self.grid[i][j] = gridBubble(GREEN,i,j,True)
				else:
					self.grid[i][j] = gridBubble(RED,i,j,True)
				self.grid[i][j].draw()
		self.appendBottom()
		#self.graph = self.makeGraph()
		self.initNeighb()
		self.test()

	def draw(self):
		for i in range(self.rows):
			for j in range(self._cols):
				if self.grid[i][j]:
					self.grid[i][j].draw()
	def check(self,bullet_pos,bullet):
		for i in range(self.rows):
			for j in range(self._cols):
				# print(str(i)+","+str(j))
				gridElement = self.grid[i][j]
				if gridElement:
					if gridElement.exists:
						dx = gridElement.pos[0] - bullet_pos[0]
						dy = gridElement.pos[1] - bullet_pos[1]
						combRadius = BUBBLE_RADIUS * 2
						if((int(dx)**2)+(int(dy)**2)<int(combRadius)**2):
							bullet.getGridPos(self)
						else:
							pass
		#Check if the bottom row is completely null, if not, add a null row
		for j in range(self._cols):
			if self.grid[self.rows-1][j].exists:
				self.appendBottom()

	def checkGameOver(self,game):
		if self.rows == 20:
			game.over == True
			#self.grid[i][j].color = WHITE
	def appendBottom(self):
		row = []
		for j in range(self._cols):
			row.append(gridBubble(BLACK,self.rows,j,False))
		self.grid.append(row)	
		self.rows += 1

	def initNeighb(self):

		for row in range(self.rows):
			for col in range(self._cols):

				if row % 2 != 0:
					if col > 0:
						self.grid[row][col].L = (row, col - 1)

					if col < (self._cols - 1):
						self.grid[row][col].R = (row,col + 1)

					if row > 0:

						self.grid[row][col].UR = (row - 1,col)

						if col > 0:
							self.grid[row][col].UL = (row - 1,col - 1)

					if row < (self.rows - 1):
						self.grid[row][col].DR = (row + 1, col)

						if col > 0:
							self.grid[row][col].DL = (row + 1,col - 1)					
							


				if row % 2 == 0:
					if col > 0:
						self.grid[row][col].L = (row, col - 1)

					if col < (self._cols - 1):
						self.grid[row][col].R = (row,col + 1)

					if row > 0:
						self.grid[row][col].UL = (row - 1,col)

						if col < (self._cols - 1):
							self.grid[row][col].UR = (row - 1,col + 1)

					if row < (self.rows - 1):
						self.grid[row][col].DL = (row + 1,col)

						if col < (self._cols - 1):
							self.grid[row][col].DR = (row + 1, col + 1)

		return

	def test(self):

		# for row in range(self.rows):
		# 	for col in range(self._cols):
		# 		print("(row, col): ({} {})".format(row, col))
		# 		print(self.grid[row][col].getNeighbs())

		reached = self.search(self.grid[0][0])

		

		for bubble in reached:
			print('(row,col): ({},{})'.format(bubble.row, bubble.col))

		return

	def search(self, bubble, reached = None):

		print(bubble)
		

		if reached == None: reached = []

		if bubble in reached: return

		reached.append(bubble)

		for neighb in bubble.getNeighbs():
			new_bubble = self.grid[neighb[0]][neighb[1]]

			if new_bubble.exists:
				if new_bubble.color == bubble.color:
					self.search(new_bubble, reached)

		return reached



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