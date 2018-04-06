import time, random
import pygame as pg
from math import *
from constants import *
#pretty easy to implement if we so choose
#from collections import deque
pg.init()


#grid

#create display
display = pg.display.set_mode((DISP_W,DISP_H))

# Change title of window
pg.display.set_caption(CAPTION)

# Game specific clock
clock = pg.time.Clock()

class bubble():
	def __init__(self,color,pos):
		self.diameter = BUBBLE_DIAMETER
		self.color = color
		self.pos = pos
	def draw(self):
		pg.draw.circle(display,self.color,
			(int(self.pos[0]),int(self.pos[1])),self.diameter)

class gridBubble(bubble):
	def __init__(self,color,pos,row,col):
		bubble.__init__(self,color,pos)
		self.row = row
		self.col = col
		self.calcPos()
	def calcPos(self):
		x = (self.col * ((ROOM_WIDTH-BUBBLE_DIAMETER) / (GRID_COLS)))+WALL_BOUND_L+BUBBLE_DIAMETER
		if self.row%2 == 0:
			x+=BUBBLE_DIAMETER
		y = BUBBLE_DIAMETER + self.row*BUBBLE_DIAMETER*2
		self.pos = (x,y)

class bullet(bubble):
	def __init__(self,color,pos,angle):
		bubble.__init__(self,color,pos)
		self.x_vel = cos(angle) * BUBBLE_VEL
		self.y_vel = sin(angle) * BUBBLE_VEL
		self.out_of_bounds = False
	def updatePos(self):
		if self.pos[0]-BUBBLE_DIAMETER <= WALL_BOUND_L:
			self.x_vel = self.x_vel * -1
		elif self.pos[0]+BUBBLE_DIAMETER >= WALL_BOUND_R:
			self.x_vel = self.x_vel * -1
		x_pos = self.pos[0]
		y_pos = self.pos[1]
		x_pos += self.x_vel
		y_pos -= self.y_vel
		self.pos = (x_pos,y_pos)
		if self.pos[1] <= 0:
			self.out_of_bounds = True
		else:
			self.out_of_bounds = False
		self.draw()
	def getGridPos(self,grid):
		for i in range(grid.rows):	
			for j in range(grid.cols):
				#Check if balls x is within a given slot
				if not grid.grid[i][j]:
					print("SFDFDS")
					if grid.grid[i][j].pos[0]-BUBBLE_DIAMETER<self.pos[0]<grid.grid[i][j].pos[0]+BUBBLE_DIAMETER:
						if grid.grid[i][j].pos[1]-BUBBLE_DIAMETER<self.pos[0]<grid.grid[i][j].pos[0]+BUBBLE_DIAMETER:
							print("HIT")
							print(str(i)+","+str(j))
	#TODO: implement a function that takes postions and snaps it onto the grid.
	

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
	#return angle
#------------------------------------------------------------
#make grid object(?)
#make grid a set pattern(?)
class gameGrid():
	def __init__(self):
		self.rows = GRID_ROWS
		self.cols = GRID_COLS
		self.grid = [[0 for x in range(GRID_COLS)] for y in range(GRID_ROWS)]
		for i in range(GRID_ROWS):
			for j in range(GRID_COLS):
				self.grid[i][j] = gridBubble(GREEN,None,i,j)
				self.grid[i][j].draw()
		self.appendBottom()
	def draw(self):
		for i in range(self.rows):
			for j in range(GRID_COLS):
				print(str(i)+","+str(j))
				if self.grid[i][j]:
					self.grid[i][j].draw()
	def check(self,bullet_pos,bullet):
		for i in range(self.rows):
			for j in range(GRID_COLS):
				# print(str(i)+","+str(j))
				gridElement = self.grid[i][j]
				if gridElement:
					dx = gridElement.pos[0] - bullet_pos[0]
					dy = gridElement.pos[1] - bullet_pos[1]
					combRadius = BUBBLE_DIAMETER * 2
					# print(str((int(dx)**2)+(int(dy)**2)))
					# print("DD")
					# print(str(int(dx)^2))
					#if intersecting
					if((int(dx)**2)+(int(dy)**2)<int(combRadius)**2):
						bullet.getGridPos(self)
					else:
						self.grid[i][j].color = WHITE
	def appendBottom(self):
		row = []
		for j in range(GRID_COLS):
			row.append(None)
		self.grid[self.cols].append(row)
		self.rows += 1


def main():
	#print('program start')
	mouse_angle = pi/2
	gameBullet = None
	gamegrid = gameGrid()
	preBullet = bubble(BALL_COLOURS[random.randint(0,len(BALL_COLOURS)-1)],ARROW_BASE)
	preBullet.draw()
	while True:
		drawBackground()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()
				mouse_angle = calcMouseAngle(mouse_pos)
				
			if event.type == pg.MOUSEBUTTONDOWN:
				#TODO: Implement singleton
				if gameBullet:
					pass
				else:
					gameBullet = bullet(preBullet.color,calcArrowHead(mouse_angle),mouse_angle)
					preBullet = bubble(BALL_COLOURS[random.randint(0,len(BALL_COLOURS)-1)],ARROW_BASE)
					preBullet.draw()
					gameBullet.draw()

			#Ctrl+C to quit
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.quit()
					quit()
		#Draw arrow
		drawArrow(mouse_angle)
		#sudo singleton, should become actual singleton if we get time
		if gameBullet:
			gameBullet.updatePos()
			gamegrid.check(gameBullet.pos,gameBullet)
			if gameBullet.out_of_bounds:
				gameBullet = None
		#Check for collision
		
		preBullet.draw()
		gamegrid.draw()
		pg.display.update()
		clock.tick(60)
	return

	pg.draw.circle(display,self.color,
			(int(self.pos[0]),int(self.pos[1])),self.diameter)

if __name__ == '__main__':
	main()