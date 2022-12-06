
import pygame
import os
import time
import threading as th
import pickle
import math
import json
import discogs_client
import coverlovin2
import requests

dc = discogs_client.Client('ExampleApplication/0.1',user_token="AFgBxqbEvFlOWRwIcGtqrRGANUttwrfzncekMGbi")

import pathlib
# fp = "/Users/alainrochette/MyGit/Personal/RB/"
fp = ""

def inKeys(keys, L):
	if isinstance(keys, list):
		return any(key in L for key in keys)
	return keys in L

controlPads = {2: "snare", 3: "hihat", 0: "tom", 1: "crash", 4: "kick", 12: "home", 8: "select", 9: "start", 69: "openhihat"}
padControls = {"snare":2,  "hihat":3,  "tom":0,  "crash":1,  "kick":4,  "home":12, "select":8,  "start":9, "openhihat": 69}
drumControls = {"snare":2,  "hihat":3,  "tom":0,  "crash":1,  "kick":4, "openhihat": 69}

drumPads = {2: "snare", 3: "hihat", 0: "tom", 1: "crash", 4: "kick"}
controlKeys = {pygame.K_DOWN: "down",
				pygame.K_UP: "up",
				pygame.K_LEFT: "left",
				pygame.K_RIGHT: "right",
				pygame.K_RETURN: "crash",
				pygame.K_BACKSPACE: "home",
				pygame.K_SPACE: "start",
				pygame.K_c: "select"}

drumKeys = {	pygame.K_a: "kick",
				pygame.K_s: "snare",
				pygame.K_j: "hihat",
				pygame.K_k: "tom",
				pygame.K_l: "crash"}

DPAD = {(0, 1): "up", (0, -1): "down", (-1,0): "left", (1,0): "right"}


compKeys = {**controlKeys, **drumKeys}
# allPads = {**controlPads, **DPAD}
allPads = {**controlPads, **DPAD, **controlKeys, **drumKeys}

# if pygame.joystick.get_count() == 0: allPads = {**controlPads, **DPAD, **controlKeys, **drumKeys}

YELLOW = ( 255, 237, 51)
BLUE = (0,0,205)
LIGHTBLUE = (100,80,255)
ORANGE = ( 255, 183, 51)
RED = (205, 0, 0)
LIGHTRED = (245, 80, 80)
GREEN = (0, 205, 0 )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (80,80,80)
W = 1280
H = 740
res = 10
