
# import pygame
# import os
# import time
# import threading as th
# import pickle
# import math
# import json
# import discogs_client
# import coverlovin2
# import requests
import pygame
import os
fp = os.path.dirname(__file__) + "/"


api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'


S_WIDTH = 1280
S_HEIGHT = 1919
LEFT_ARROW = 2
RIGHT_ARROW = 3
UP_ARROW = 0
DOWN_ARROW = 1
BACKSPACE = 127
A_KEY = 97
S_KEY = 115
W_KEY = 119
D_KEY = 100
WOULD_WATCH = W_KEY = 119
HAVENT_SEEN = S_KEY = 115
LIKED = D_KEY = 100
DIDNT_LIKE = A_KEY = 97
EXIT = 27

SELECT_TIMER = 1

BUTTON_RADIUS = 80
BUTTON_COLOR = (255,255,255)
TEXT_COLOR = (0,0,0)
BUTTON_THICKNESS = 1

WOULD_WATCH_CENTER = (S_WIDTH//2,int(S_HEIGHT*9/10)-2*BUTTON_RADIUS)
HAVENT_SEEN_CENTER = (S_WIDTH//2,int(S_HEIGHT*9/10))
LIKED_CENTER = (int(S_WIDTH*(3/4)),int(S_HEIGHT*9/10))
DIDNT_LIKE_CENTER = (int(S_WIDTH*1/4),int(S_HEIGHT*9/10))


HAVENT_SEEN_COLOR = (0,0,0)
WOULD_WATCH_COLOR = (50,80,50)
LIKED_COLOR = (150,255,150)
DIDNT_LIKE_COLOR = (150,150,255)
SELECTED_THICKNESS = 20


YELLOW = ( 255, 237, 51)
BLUE = (0,0,205)
LIGHTBLUE = (100,80,255)
ORANGE = ( 255, 183, 51)
RED = (205, 0, 0)
LIGHTRED = (245, 80, 80)
GREEN = (0, 205, 0 )
DARKGREEN = (0, 60, 0 )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (80,80,80)
LIGHTGREY = (120,120,120)
W = 1280
H = 740
res = 10

FONTattr = fp + 'Assets/Fonts/UNI.otf', 40 * int(H / 740)

def inKeys(keys, L):
	if isinstance(keys, list):
		return any(key in L for key in keys)
	return keys in L


compKeys = {pygame.K_DOWN: "down",
				pygame.K_UP: "up",
				pygame.K_LEFT: "left",
				pygame.K_RIGHT: "right",
				pygame.K_RETURN: "crash",
				pygame.K_BACKSPACE: "home",
				pygame.K_SPACE: "start",
				pygame.K_c: "select"}