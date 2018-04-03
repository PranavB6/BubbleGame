import time, random
import pygame as pg
from math import *
from constants import *
pg.init()

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
		# print("X: "+str(self.x_vel))
		# print("Y: "+str(self.y_vel))
		# print("POS"+(str(self.pos)))
		x_pos = self.pos[0]
		y_pos = self.pos[1]
		x_pos += self.x_vel
		y_pos -= self.y_vel
		self.pos = (x_pos,y_pos)

		if self.pos[1]-BUBBLE_DIAMETER <= 0:
			self.out_of_bounds = True
		else:
			self.out_of_bounds = False
		print("POST"+str(self.pos))
		self.draw()

def drawBackground():
	display.fill(LIGHT_GRAY)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)

def drawArrow(arrow_angle):
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

def main():
	print('program start')
	mouse_angle = pi/2
	gameBullet = None
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
		drawArrow(mouse_angle)

		if gameBullet:
			gameBullet.updatePos()
			if gameBullet.out_of_bounds:
				gameBullet = None
		preBullet.draw()
		pg.display.update()
		clock.tick(60)
	return

	pg.draw.circle(display,self.color,
			(int(self.pos[0]),int(self.pos[1])),self.diameter)

if __name__ == '__main__':
	main()
