import time, random
import pygame as pg
from math import *
from constants import *
from bubble import *
import time, string


class StateMachine():

	def __init__(self):

		self.states = ['begin', 'next_key', 'final_key', 'reset']
		self.state = 'begin'
		self.idx = 0

	def set(self, state):

		if state not in self.states: raise ValueError('{} not a valid state'.format(state))
		else: self.state = state

		# print('State set to', self.state)

	def get_state(self):
		return self.state



class cheatManager():


	def __init__(self, gamegrid, gun):
		self.gamegrid = gamegrid
		self.gun = gun 
		self.alphabet = set(string.ascii_lowercase)
		self.explosion = False

		#----------------------------------- Put you cheat codes here --------------------------------#
		self.cheats = ['god', 'stevejobs', 'explosion', 'LOL']

		self.machines = [StateMachine() for cheat in self.cheats]

	def view(self, event):

		for idx in range(len(self.cheats)):
			self.check(event, self.cheats[idx], self.machines[idx])

	def check(self, event, cheat, machine):

		char = chr(event.key)

		if char not in self.alphabet: return

		# print('Pressed:', char)

		if machine.get_state() == 'begin':
			machine.idx = 0
			if char == cheat[machine.idx]:
				machine.set('next_key') 
				machine.idx += 1
			return

		if machine.get_state() == 'next_key':

			# print('char', char)
			# print('cheat[{}] = {}'.format(machine.idx, cheat[machine.idx] ))
			if char == cheat[machine.idx]:
				machine.idx += 1

				if machine.idx + 1 == len(cheat):
					machine.set('final_key')
					

			else: machine.set('begin')
				
			return

		if machine.get_state() == 'final_key':
			if char == cheat[machine.idx]:

				for machine in self.machines:
					machine.set('begin')

				#-------------------------------- Put cheat functions here --------------------------#
				if   cheat == 'god': self.god_cheat()
				elif cheat == 'LOL': self.lol_cheat()
				elif cheat == 'stevejobs': self.saviour_cheat()
				elif cheat == 'explosion': self.explosion_cheat()
				else: print('Bruh, this cheat don\'t have a function:', cheat )
				#------------------------------------------------------------------------------------#

			else: machine.set('begin')

			return

	#-------------------------------------------------- Put what the cheat function do here -------------------------- #

	def god_cheat(self):
		print('Entering God Mode')

		for row in range(self.gamegrid.rows):
			for col in range(self.gamegrid._cols):
				if self.gamegrid.grid[row][col].exists:
					self.gamegrid.grid[row][col].color = self.gun.loaded.color

	def lol_cheat(self):
		print('lol')

	def saviour_cheat(self):
		print('I LOVE APPLE AND APPLE LOVES ME')

	def explosion_cheat(self):
		print('Activated Cheat: Explosion')
		self.gun.loaded.color = BLACK
		self.gun.explosion = True



class game():
	def __init__(self):
		self.over = False
		self.score = 0
		self.running = False
		self.ballCounter = 0
		
	#Check game over if grid rows exceed a given amount
	def checkGameOver(self,grid,clock,game):
		if self.over == True:
			return
		if grid.rows >= GAMEOVER_ROWS:
			for col in range(grid._cols):
				if grid.grid[GAMEOVER_ROWS-1][col].exists:
					for row in range(grid.rows):
						for col in range(grid._cols):
							if grid.grid[row][col].exists:
								grid.grid[row][col].popSelf(grid)

					drawBackground()
					grid.draw(game)
					pg.display.update()
					clock.tick(60)
					self.over = True


			
class gameGrid():
	def __init__(self,game):
		self.rows = GRID_ROWS
		self._cols = GRID_COLS
		self.grid = [[0 for x in range(self._cols)] for y in range(self.rows)]
		self.even_offset = True
		colorInd = 0
		self.animations = []

		for i in range(self.rows):
			for j in range(self._cols):
				self.grid[i][j] = gridBubble(random.choice(BALL_COLOURS),i,j,True, self)
				self.grid[i][j].draw(game)
		self.initNeighbGrid()

	def draw(self,game):
		for i in range(self.rows):
			for j in range(self._cols):
				if self.grid[i][j]:
					# print('(row, col) = {}, {})'.format(i, j))
					self.grid[i][j].draw(game)

		for animation in self.animations:
			if not animation: 
				self.animations.remove(animation)
				continue
			frame = animation.pop()
			frame.draw(game)

	def check(self,bullet_pos,bullet,game):
		if bullet == None or bullet.out_of_bounds:
			return
		for i in range(self.rows):
			for j in range(self._cols):
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
								self.grid[bulletGridPos[0]][bulletGridPos[1]].initNeighb(self)
								self.grid[bulletGridPos[0]][bulletGridPos[1]].updateNeighbs(self)
								

								game.ballCounter += 1
								if game.ballCounter % APPEND_COUNTDOWN == 0:
									self.appendTop()

								if bullet.explosion: 
									for neighb in self.grid[bulletGridPos[0]][bulletGridPos[1]].getNeighbs():
										self.popCluster(neighb, game)
										self.grid[neighb[0]][neighb[1]].popSelf(self)

									self.grid[bulletGridPos[0]][bulletGridPos[1]].popSelf(self)

									self.initNeighbGrid()

									bullet.explosion = False
								else: 
									self.popCluster(bulletGridPos,game)

								return
						else:
							pass
		if bullet_pos[1]-BUBBLE_RADIUS < 0:
			bulletGridPos = bullet.getGridPos(self)
			if bulletGridPos:
				self.grid[bulletGridPos[0]][bulletGridPos[1]].initNeighb(self)
				self.grid[bulletGridPos[0]][bulletGridPos[1]].updateNeighbs(self)
				self.popCluster(bulletGridPos,game)
				return
			else:
				bullet.out_of_bounds = True
		#Check if the bottom row is completely null, if not, add a null row
		for j in range(self._cols):
			if self.grid[self.rows-1][j].exists:
				self.appendBottom()

	def appendBottom(self):
		row = []
		color = BG_COLOUR

		# if self.rows <= 17:
		# 	color = BG_COLOUR
		# else:
		# 	color = MIDDLE_GRAY
		for j in range(self._cols):
			row.append(gridBubble(color,self.rows,j,False, self))
		self.grid.append(row)	
		self.rows += 1

	def initNeighbGrid(self):
		for row in range(self.rows):
			for col in range(self._cols):
				self.grid[row][col].initNeighb(self)

		return

	def popCluster(self,bulletGridPos,game):
		
		pop = False
		to_pop = []
		to_pop_n = 0

		# print('Blast point:', bulletGridPos[0], bulletGridPos[1] )
		reached = self.search(self.grid[bulletGridPos[0]][bulletGridPos[1]])
		# print()

		rooted = self.rootSearch(self.grid[bulletGridPos[0]][bulletGridPos[1]])

		if len(reached)>=3: pop = True

		if pop:
			to_pop_n = len(reached)
			for bubble in reached: to_pop.append(bubble)

			while to_pop_n:
				to_pop_n -= 1
				bubble = to_pop.pop()
				if bubble.exists:
					bubble.popSelf(self)
					game.score += 1
				bubble.updateNeighbs(self)

				for neighb in bubble.getNeighbs():
					rooted = self.rootSearch(self.grid[neighb[0]][neighb[1]]) 
					if not rooted:
						to_pop.append(self.grid[neighb[0]][neighb[1]])
						to_pop_n += 1
		return

	def search(self, bubble, reached = None):

		if reached == None: 
			reached = []

		if bubble in reached: return

		reached.append(bubble)

		for neighb in bubble.getNeighbs():
			new_bubble = self.grid[neighb[0]][neighb[1]]

			if new_bubble.exists:
				if new_bubble.color == bubble.color:
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
		new_bubbles = [gridBubble(random.choice(BALL_COLOURS),0,col,True, self) for col in range(self._cols) ]

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


# bg = pg.image.load('bg.jpg').convert()
bg = pg.image.load('bg.png').convert()
_, _, bg_w, bg_h = bg.get_rect()
sf = 0.8
bg = pg.transform.scale(bg, (int(bg_w * sf), int(bg_h * sf)))

def drawBackground():
	display.blit(bg, (0,0))
	pg.draw.line(display, BLUE, (WALL_BOUND_L, 0), (WALL_BOUND_L, DISP_H))
	pg.draw.line(display, BLUE, (WALL_BOUND_R, 0), (WALL_BOUND_R, DISP_H))
	pg.draw.line(display, RED, (WALL_BOUND_L, DISP_H - FLOOR_HEIGHT), (WALL_BOUND_R, DISP_H - FLOOR_HEIGHT))
	# pg.draw.rect(display,MIDDLE_GRAY,WALL_RECT_FLOOR)
	# pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	# pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)
	wall = pg.Surface((WALL_WIDTH,DISP_H), pygame.SRCALPHA, 32)
	floor = pg.Surface((ROOM_WIDTH,FLOOR_HEIGHT),pygame.SRCALPHA, 32)
	wall.fill((122,122,122,122))
	floor.fill((200,0,0,90))
	display.blit(floor,(WALL_BOUND_L,WALL_BOUND_FLOOR))
	display.blit(wall,(0,0))
	display.blit(wall,(WALL_BOUND_R,0))

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

crosshair = pygame.image.load('crosshair.png')
# Scale image
sf = 00.20
crosshair = pg.transform.scale(crosshair, (int(crosshair.get_width() * sf), int(crosshair.get_height() * sf)))
crosshair_rect = crosshair.get_rect()

def drawCursor(mouse_pos):
	crosshair_rect.center = mouse_pos
	display.blit(crosshair, crosshair_rect)

# outlinePosition = [-1,0,1]
# def giveOutline(text,position,outlineSize):
# 	for xDisplacement in outlinePosition:
# 		for yDisplacement in outlinePosition:
# 			display.blit(text,(position[0]+xDisplacement*outlineSize,position[1]+yDisplacement*outlineSize))
