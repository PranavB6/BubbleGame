import time, random
import pygame as pg
from math import *
from constants import *
from bubble import *
import time

class game():
	def __init__(self):
		self.over = False
		self.score = 0
	#Check game over if grid rows exceed a given amount
	def checkGameOver(self,grid):
		if grid.rows >= GAMEOVER_ROWS:
			print("GAME OVER")
			self.over = True
class gameGrid():
	def __init__(self):
		self.rows = GRID_ROWS
		self._cols = GRID_COLS
		self.grid = [[0 for x in range(self._cols)] for y in range(self.rows)]
		self.even_offset = True
		for i in range(self.rows):
			for j in range(self._cols):
				if j%2 == 0:
					randColor = random.choice(BALL_COLOURS)

				self.grid[i][j] = gridBubble(randColor,i,j,True, self)
				self.grid[i][j].draw()
		self.appendBottom()
		self.initNeighbGrid()
		self.appendTop()
	def draw(self):
		for i in range(self.rows):
			for j in range(self._cols):
				if self.grid[i][j]:
					self.grid[i][j].draw()
	def check(self,bullet_pos,bullet,game):
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
							##BULLET HITS GRID##
							bulletGridPos = bullet.getGridPos(self)
							
							if bulletGridPos:

								# print('-------------------------------')
								# print('Bullet Grid Position:', bulletGridPos[0], bulletGridPos[1] )
								self.grid[bulletGridPos[0]][bulletGridPos[1]].initNeighb(self)
								self.grid[bulletGridPos[0]][bulletGridPos[1]].updateNeighbs(self)


								#print (self.grid[bulletGridPos[0]][bulletGridPos[1]].getNeighbs())
								self.popCluster(bulletGridPos,game)

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
			row.append(gridBubble(BLACK,self.rows,j,False, self))
		self.grid.append(row)	
		self.rows += 1

	def initNeighbGrid(self):
		for row in range(self.rows):
			for col in range(self._cols):
				self.grid[row][col].initNeighb(self)

		return

	def test(self):
		global EvenOffset
		for row in range(self.rows):
			for col in range(self._cols):
				print("(row, col): ({} {}) Color: {}".format(row, col, self.grid[row][col].color))
				print(self.grid[row][col].getNeighbs())
		# reached = self.test(self.grid[0][0])
		# for bubble in reached:
		# 	pass
		# 	#print('(row,col): ({},{})'.format(bubble.row, bubble.col))
		# return
		return

	def popCluster(self,bulletGridPos,game):
		
		pop = False
		to_pop = []
		to_pop_n = 0

		# print('Blast point:', bulletGridPos[0], bulletGridPos[1] )
		reached = self.search(self.grid[bulletGridPos[0]][bulletGridPos[1]])
		# print()

		rooted = self.rootSearch(self.grid[bulletGridPos[0]][bulletGridPos[1]])

		print('{} rooted: {}, exists: {}'.format(bulletGridPos, rooted, self.grid[bulletGridPos[0]][bulletGridPos[1]].exists) )

		if len(reached)>=3: pop = True

		if pop:
			to_pop_n = len(reached)
			for bubble in reached: to_pop.append(bubble)

			while to_pop_n:
				to_pop_n -= 1
				bubble = to_pop.pop()
				if bubble.exists:
					bubble.popSelf()
					game.score += 1
					print(game.score)
				bubble.updateNeighbs(self)

				for neighb in bubble.getNeighbs():
					rooted = self.rootSearch(self.grid[neighb[0]][neighb[1]]) 
					if not rooted:
						print('Not rooted:', neighb)
						to_pop.append(self.grid[neighb[0]][neighb[1]])
						to_pop_n += 1
		return

	def search(self, bubble, reached = None):

		#print(bubble)
		

		if reached == None: 
			reached = []

			# print('Comrads:', end = ' ')
		if bubble in reached: return

		reached.append(bubble)

		for neighb in bubble.getNeighbs():
			new_bubble = self.grid[neighb[0]][neighb[1]]

			if new_bubble.exists:
				if new_bubble.color == bubble.color:
					# print('({},{})'.format(new_bubble.row, new_bubble.col), end = ' ')
					self.search(new_bubble, reached)	

		return reached

	def appendTop(self):

		self.even_offset = not self.even_offset
		
		for row in range(self.rows):
			for col in range(self._cols):
				# print('(row, col) = ({}, {})'.format(row, col))
				self.grid[row][col].row += 1
				self.grid[row][col].calcPos(self)

		self.rows += 1

		new_bubbles = [gridBubble(YELLOW,0,col,True, self) for col in range(self._cols) ]

		self.grid.insert(0, new_bubbles)

		for row in range(self.rows):
			for col in range(self._cols):
				self.grid[row][col].initNeighb(self)

		return

	def rootSearch(self, bubble, rooted = False, reached = None):

		if reached == None: reached = []

		if bubble not in reached:
			reached.append(bubble)

			if bubble.row == 0: 
				rooted = True 

			else:
				for neighb in bubble.getNeighbs():
					rooted = self.rootSearch(self.grid[neighb[0]][neighb[1]], rooted, reached)

		return rooted



def drawBackground():
	display.fill(BG_COLOUR)
	pg.draw.rect(display,MIDDLE_GRAY,WALL_RECT_FLOOR)
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