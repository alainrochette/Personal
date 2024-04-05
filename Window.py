#!/usr/bin/env python
# from variables import *
import pygame
import pygame_menu


from Database import *
from TVShow import *
from variables import *
from Menu import *


pygame.init()

os.environ["SDL_VIDEODRIVER"] = "dummy"

# WINDOW_SIZE = [W, H]


pygame.mouse.set_visible(True)


info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
W,H = info.current_w,info.current_h
# screen = pygame.display.set_mode([W,H], pygame.FULLSCREEN)
screen = pygame.display.set_mode([W,H])
# pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
menu = Menu(screen, clock, [W,H])

while not menu.done:


	# Clear the screen
	# pygame.display.toggle_fullscreen()
	menu.update()
	clock.tick(200)
	pygame.display.flip()

for movie in menu.DB.myDB["All Movies"]:
	try: 
		x = int(movie.myRating)
		movie.myRating = min(2,movie.myRating)
	except: 
		movie.myRating = 0
	
watched = list(filter(lambda x: x.watched, menu.DB.myDB["All TV Shows"]))
names =  list(sorted( watched, key=lambda x: x.name, reverse=False))
x =  list(sorted( names, key=lambda x: 0 if x.myRating == None else x.myRating, reverse=True))
ratingDict = {2: "weeena ctm have fun",1: "it's culturally significant and/or entertaining, dope choice, have fun", 0:"it's a movie, have fun!", -1: "i wouldn't do that but have fun", -2: "do not do that"}
currRating = "X"
print("If you tell alain that you are going to watch this movie, he will say:")
for movie in x:
	rating = movie.myRating
	
	if rating != currRating:
		currRating = rating
		print("")
		print("*{}*".format(ratingDict[int(rating)]))
		print("")
	
	print("{} ({})".format(movie.name, movie.date[0:4]))

print("")
print("Watchlist")
print("")
watchList = list(filter(lambda x: x.on_watchlist and not x.watched, menu.DB.myDB["All Movies"]))
names =  list(sorted( watchList, key=lambda x: x.name, reverse=False))
for movie in names:
	print("{} ({})".format(movie.name, movie.date[0:4]))
# with open(fp + 'cache/Preferences.txt', 'wb') as fp:
# 		pickle.dump({"lag": menu.lag}, fp)

numWatched = len(list(filter(lambda x: x.watched, menu.DB.myDB["All TV Shows"])))

print("")
print("Distribution")
print("")
print("Total Watched TV Shows: {}".format(numWatched))
for i in range(-2,3):
	try:
		p = len(list(filter(lambda x: x.watched and x.myRating == -1*i, menu.DB.myDB["All TV Shows"])))/numWatched
		# p_bar= "◫" * int(p*100/2) + ("▯" if p < 0.01 else "")
		print("{}: {:.0%}".format(-1*i, len(list(filter(lambda x: x.watched and x.myRating == -1*i, menu.DB.myDB["All TV Shows"])))/numWatched))
		# print("{}: {}".format(-1*i, p_bar))
	
	except:
		pass

menu.DB.saveMyDB()
pygame.quit()
# exit()
