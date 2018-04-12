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
pg.mixer.init()
pg.font.init()

#create display
display = pg.display.set_mode((DISP_W,DISP_H))

# Change title of window
pg.display.set_caption(CAPTION)

# Game specific clock
clock = pg.time.Clock()

font = pg.font.Font("pixel.otf", 30)

gun = Shooter(pos = BOTTOM_CENTER)
gun.putInBox()


pg.mixer.music.load('hatsune_miku_love_and_dreams.mp3')
#invis cursor
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

def main():
	screenShake = [-1,0,1]
	gameInstance = game()
	mouse_angle = pi/2
	gameBullet = None
	gamegrid = gameGrid(gameInstance)
	mouse_pos=(DISP_W/2, DISP_H/2)
	scoreLabel = font.render("Score:",True,BLACK)
	startLabel = font.render("Press Left Click To Start",True,BLACK)
	endLabel = font.render("Loser Is You",True,BLACK)
	endPrompt = font.render("Press R to restart",True,BLACK)
	pygame.mixer.music.play(-1)
	cheat_manager = cheatManager(gamegrid, gun)
	while True:
		scoreNum = font.render(str(gameInstance.score),True,BLACK)
		drawBackground()
		display.blit(scoreNum,(WALL_BOUND_R-(scoreNum.get_width()/2)+WALL_WIDTH/2,120))
		display.blit(scoreLabel,(WALL_BOUND_R-(scoreLabel.get_width()/2)+WALL_WIDTH/2,90))
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.KEYDOWN:
				#Have cheat manager view key events
				cheat_manager.view(event)

				#Ctrl+C to quit
				if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.quit()
					quit()
				#r or R to restart
				if event.key == pg.K_r or pg.K_r and pg.key.get_mods() & pg.KMOD_SHIFT:
					if gameInstance.over:
						return

			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()
				mouse_angle = calcMouseAngle(mouse_pos)

			#Lock game specific controls if game is over
			if gameInstance.over:
				break
			
			if event.type == pg.MOUSEBUTTONDOWN:
				if not gameInstance.running:
					gameInstance.running = True
				if gameBullet:
					pass
				else:
					gun.fire()

		if gun.fired:
			gamegrid.check(gun.fired.pos,gun.fired,gameInstance)

		#Draw all balls in the grid
		gamegrid.draw(gameInstance)

		#rotate gun and draw accordningly based mon mouses position
		gun.rotate(mouse_pos)
		gun.draw_bullet(gameInstance)
		#Check the game if its over (ie. rows exceed the given threshold)
		gameInstance.checkGameOver(gamegrid,clock,game)

		#Give starting prompt when game isn't running
		if not gameInstance.running:
			display.blit(startLabel,(DISP_W/2-(startLabel.get_width()/2),DISP_W/2))

		#Display gameover text if game is over.
		if gameInstance.over:
			display.blit(endLabel,(DISP_W/2-(endLabel.get_width()/2)+random.choice(screenShake),DISP_H/2-30+random.choice(screenShake)) )
			scoreNumEnd = font.render("Score: "+str(gameInstance.score),True,BLACK)
			display.blit(scoreNumEnd,(DISP_W/2-(scoreNumEnd.get_width()/2)+random.choice(screenShake),DISP_H/2+random.choice(screenShake)) )
			display.blit(endPrompt,(DISP_W/2-(endPrompt.get_width()/2)+random.choice(screenShake),DISP_H/2+30+random.choice(screenShake)) )

		drawCursor(mouse_pos)
		pg.display.update()
		clock.tick(60)
	return

if __name__ == '__main__':
	#Call main in True loop to allow it to reset it self if. main returns when r is pressed.
	while True:
		main()