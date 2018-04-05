from constants import *
import math, random
import pygame as pg
pg.init()

class gameGrid():
	def __init__(self):
		self.rows = GRID_ROWS
		self.grid = [[0]*GRID_COLS]*GRID_ROWS
		for i in range(0,GRID_ROWS):
			for j in range(0,GRID_COLS):
				self.grid[i][j] = gridBubble(GREEN,None,i,j)
				# print(self.grid[i][j])
				self.grid[i][j].draw()
	def draw(self):
		# print("START")
		for i in range(0,GRID_ROWS):
			for j in range(0,GRID_COLS):
				self.grid[i][j] = gridBubble(WHITE,None,i,j)
				# print(self.grid[i][j].pos)
				self.grid[i][j].draw()
				if self.grid[i][j]:
					self.grid[i][j].draw()
		# print("END")

	def check(self,bullet_pos):
		for i in range(0,GRID_ROWS):
			for j in range(0,GRID_COLS):
				gridElement = self.grid[i][j]
				if gridElement:
					dx = gridElement.pos[0] - bullet_pos[0]
					dy = gridElement.pos[1] - bullet_pos[1]
					combRadius = BUBBLE_DIAMETER * 2
					if((int(dx)^2)+(int(dy)^2)<int(combRadius)^2):
						self.grid[i][j].color = RED
					else:
						self.grid[i][j].color = WHITE