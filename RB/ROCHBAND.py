#!/usr/bin/env python

import pygame

pygame.init()


from Song import *
from Player import *
from variables import *
from Menu import *

# WINDOW_SIZE = [W, H]


# pygame.mouse.set_visible(False)


info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
W,H = info.current_w,info.current_h
screen = pygame.display.set_mode([W,H], pygame.FULLSCREEN)

# pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
menu = Menu(screen, clock, [W,H])
while not menu.done:


	# Clear the screen
	# pygame.display.toggle_fullscreen()
	menu.update()
	clock.tick(100)
	pygame.display.flip()


with open(fp + 'cache/Preferences.txt', 'wb') as fp:
		pickle.dump({"lag": menu.lag}, fp)

pygame.quit()
