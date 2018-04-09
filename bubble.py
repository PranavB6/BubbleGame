from constants import *



class bubble():
	def __init__(self,color,pos):
		self.radius= BUBBLE_RADIUS
		self.color = color
		self.pos = pos
	def draw(self):
		pg.draw.circle(display,self.color,
			(int(self.pos[0]),int(self.pos[1])),self.radius)

class gridBubble(bubble):

	def __init__(self,color,row,col,exists, grid):
		self.row = row
		self.col = col
		self.exists = exists
		self.calcPos(grid)
		bubble.__init__(self,color,self.pos)

		# self.id = id_Count
		# id_Count += 1

		self.L = None
		self.R = None
		self.UL = None
		self.UR = None
		self.DL = None
		self.DR = None 

	def calcPos(self, grid):
		x = (self.col * ((ROOM_WIDTH-BUBBLE_RADIUS) / (GRID_COLS)))+WALL_BOUND_L+BUBBLE_RADIUS

		if (self.row % 2 == grid.even_offset):
			x+=BUBBLE_RADIUS

		y = BUBBLE_RADIUS + self.row*BUBBLE_RADIUS*2
		self.pos = (x,y)

	def initNeighb(self,grid):
		# global EvenOffset

		self.L = None
		self.R = None
		self.UL = None
		self.UR = None
		self.DL = None
		self.DR = None

		even_offset = grid.even_offset

		if self.col > 0:
			if grid.grid[self.row][self.col-1].exists:
				self.L = (self.row, self.col - 1)

		if self.col < (grid._cols - 1):
			if grid.grid[self.row][self.col+1].exists:
				self.R = (self.row,self.col + 1)
				
	
		if self.row % 2 != even_offset:
			if self.row > 0:
				if grid.grid[self.row -1][self.col].exists:
					self.UR = (self.row - 1,self.col)
				if self.col > 0:
					if grid.grid[self.row-1][self.col-1].exists:
						self.UL = (self.row - 1,self.col - 1)

			if self.row < (grid.rows - 1):
				if grid.grid[self.row+1][self.col].exists:
					self.DR = (self.row + 1, self.col)
				if self.col > 0:
					if grid.grid[self.row+1][self.col-1].exists:
						self.DL = (self.row + 1,self.col - 1)		

		if self.row % 2 == even_offset:
			if self.row > 0:
				if grid.grid[self.row-1][self.col].exists:
					self.UL = (self.row - 1,self.col)
				if self.col < (grid._cols - 1):
					if grid.grid[self.row -1][self.col + 1].exists:
						self.UR = (self.row - 1,self.col + 1)

			if self.row < (grid.rows - 1):
				if grid.grid[self.row+1][self.col].exists:
					self.DL = (self.row + 1,self.col)
				if self.col < (grid._cols - 1):
					if grid.grid[self.row+1][self.col+1].exists:
						self.DR = (self.row + 1, self.col + 1)



	def getNeighbs(self):

		neighbs = [self.L, self.R, self.UL, self.UR, self.DL, self.DR]
		alive = []

		for neighb in neighbs:
			if neighb: alive.append(neighb)
		return alive

	def updateNeighbs(self,grid):
		neighbs = self.getNeighbs()
		for neighb in neighbs:
			grid.grid[neighb[0]][neighb[1]].initNeighb(grid)

	#MIGHT CAUSE NAMESPACE ISSUES

	def popSelf(self):
		self.exists = False
		self.color = BLACK


class bullet(bubble):
	def __init__(self,color,pos,angle):
		bubble.__init__(self,color,pos)
		self.x_vel = cos(angle) * BUBBLE_VEL
		self.y_vel = sin(angle) * BUBBLE_VEL
		self.out_of_bounds = False
	def updatePos(self):
		if self.pos[0]-BUBBLE_RADIUS <= WALL_BOUND_L:
			self.x_vel = self.x_vel * -1
		elif self.pos[0]+BUBBLE_RADIUS >= WALL_BOUND_R:
			self.x_vel = self.x_vel * -1
		x_pos = self.pos[0]
		y_pos = self.pos[1]
		x_pos += self.x_vel
		y_pos -= self.y_vel
		self.pos = (x_pos,y_pos)
		self.draw()
	def getGridPos(self,grid):
		for i in range(grid.rows):	
			for j in range(grid._cols):

				# Check if balls x is within a given slot
				if not grid.grid[i][j].exists:
					# print("SFDFDS")
					#TODO: COLLISIONS ARE NOT SPOT ON. WILL FAIL IF YOU FIRE HEAD ON.
					if grid.grid[i][j].pos[0]-BUBBLE_RADIUS<self.pos[0]<=grid.grid[i][j].pos[0]+BUBBLE_RADIUS:
						# print("PASS 1")
						if grid.grid[i][j].pos[1]-BUBBLE_RADIUS<self.pos[1]<=grid.grid[i][j].pos[1]+BUBBLE_RADIUS:
							# print("HIT")
							#print(str(i)+","+str(j))
							grid.grid[i][j].color=self.color
							grid.grid[i][j].exists=True
							self.out_of_bounds=True
							return i,j
	#TODO: implement a function that takes postions and snaps it onto the grid.