from constants import *
import math, random
from bubble_file import *
import pygame as pg
pg.init()

class gameGrid():
	def __init__(self):
		self.rows = GRID_ROWS
		self.cols = GRID_COLS

		self.grid = [[gridBubble(row, col) for col in range(self.cols)] for row in range(self.rows)]

	def draw(self):

		for row in range(self.rows):
			for col in range(self.cols):
				self.grid[row][col].draw()

	def check(self, bullet_pos):
		for i in range(self.rows):
			for j in range(self.cols):
				gridElement = self.grid[i][j]
				if gridElement:
					dx = gridElement.pos[0] - bullet_pos[0]
					dy = gridElement.pos[1] - bullet_pos[1]
					combRadius = BUBBLE_DIAMETER * 2
					if((int(dx)^2)+(int(dy)^2)<int(combRadius)^2):
						self.grid[i][j].color = RED
					else:
						self.grid[i][j].color = WHITE