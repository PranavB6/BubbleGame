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
		#NOTE: MIGHT WANT TO CHANGE X AND Y TO SINGLE POINT
		self.pos = pos
	def draw(self):
		pg.draw.circle(display,self.color,
			(int(self.pos[0]),int(self.pos[1])),self.diameter)

# class pos():
# 	def __init__(self,x_pos,y_pos):
# 		self.x = x_pos
# 		self.y = y_pos

class bullet(bubble):
	def __init__(self,color,pos,angle):
		bubble.__init__(self,color,pos)
		self.x_vel = cos(angle) * BUBBLE_VEL
		self.y_vel = sin(angle) * BUBBLE_VEL
	# def _radToXVel_(self,angle):
	# 	x_vel = cos(angle) * BUBBLE_VEL
	# 	return x_vel
	# def _radToYVel_(self,angle):
	# 	y_vel = sin(angle) * BUBBLE_VEL
	# 	return y_vel
	def updatePos(self):
		print("X: "+str(self.x_vel))
		print("Y: "+str(self.y_vel))
		print("POS"+(str(self.pos)))
		#print("POST"+str(self.pos))
		x_pos = self.pos[0]
		y_pos = self.pos[1]
		x_pos += self.x_vel
		y_pos -= self.y_vel
		self.pos = (x_pos,y_pos)
		print("POST"+str(self.pos))
		self.draw()
def drawBackground():
	display.fill(LIGHT_GRAY)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_L)
	pg.draw.rect(display,DARK_GRAY,WALL_RECT_R)
	#pg.draw.rect(display,DARK_GRAY,DEMO_RECT)


def drawArrow(arrow_angle):
	arrow_head = calcArrowHead(arrow_angle)
	pg.draw.line(display,BLACK,ARROW_BASE,arrow_head)

def calcArrowHead(arrow_angle):
	x = int(cos(arrow_angle)*ARROW_LENGTH)
	y = int(sin(arrow_angle)*ARROW_LENGTH)
	x = ARROW_BASE[0] + x
	y = ARROW_BASE[1] - y
	return (x,y)

#TODO DEFINE ANGLE LIMITS
def calcMouseAngle(mouse_pos):
	width = mouse_pos[0] - ARROW_BASE[0]
	height = (ARROW_BASE[1] - mouse_pos[1])
	angle = atan2(height,width)
	return angle

def main():
	#drawBackground()
	print('program start')
	mouse_angle = pi/2
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
				bbl =bubble(WHITE,(int(DISP_H/2),int(DISP_W/2)))
				#bbl.draw()
				gameBullet = bullet(WHITE,calcArrowHead(mouse_angle),mouse_angle)
				gameBullet.draw()

		drawArrow(mouse_angle)
		try:
 			gameBullet.updatePos()
		except NameError:
			print("Bullet not created")
			pass

		pg.display.update()
		
		clock.tick(60)
	return


if __name__ == '__main__':
	main()
