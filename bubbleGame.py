import time, random
import pygame as pg
from math import *
from constants import *
from graph import Graph
from bubble import *
from gameObj import *
from shooter_file import *
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

font = pg.font.SysFont("helvetica", 30)
bigFont  = pg.font.SysFont("helvetica",60)

gun = Shooter(pos = BOTTOM_CENTER)
gun.putInBox()

def main():

	gameInstance = game()
	mouse_angle = pi/2
	gameBullet = None
	gamegrid = gameGrid()
	mouse_pos=(0,0)
	scoreLabel = font.render("Score:",True,WHITE)
	startLabel = font.render("Press Left Click To Start",True,WHITE)
	while not gameInstance.over:
		scoreNum = font.render(str(gameInstance.score),True,WHITE)
		drawBackground()
		display.blit(scoreNum,(WALL_BOUND_R-(scoreNum.get_width()/2)+WALL_WIDTH/2,120))
		display.blit(scoreLabel,(WALL_BOUND_R-(scoreLabel.get_width()/2)+WALL_WIDTH/2,90))
		if not gameInstance.running:
			display.blit(startLabel,(DISP_W/2-(startLabel.get_width()/2),DISP_W/2))
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			#Ctrl+C to quit
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.quit()
					quit()
			#Lock game specific controls if game is over
			if gameInstance.over:
				break
			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()
				mouse_angle = calcMouseAngle(mouse_pos)
			if event.type == pg.MOUSEBUTTONDOWN:
				gameInstance.running = True
				if gameBullet:
					pass
				else:
					gun.fire()

		if gun.fired:
			gamegrid.check(gun.fired.pos,gun.fired,gameInstance)

		gamegrid.checkGameOver(gameInstance)
		gamegrid.draw()
		gun.rotate(mouse_pos)

		gun.draw_bullet()

		gameInstance.checkGameOver(gamegrid)


		pg.display.update()
		clock.tick(60)
	return

if __name__ == '__main__':
	main()