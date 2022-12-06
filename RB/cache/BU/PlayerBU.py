from variables import *
from Song import *




class Player(pygame.sprite.Sprite):

	def __init__(self,screen, Menu):
		super().__init__()
		self.menu = Menu
		self.screen = screen
		self.song = None
		self.diff = None
		self.prev = []
		self.joystick_count = pygame.joystick.get_count()
		self.editBarColor = self.menu.theme_opp
		self.edit = False
		if self.joystick_count == 0:
			pass
		else:
			# Use joystick #0 and initialize it
			self.my_joystick = pygame.joystick.Joystick(0)
			self.my_joystick.init()

	def toggleEdit(self):
		if self.song.editting:
			self.editBarColor = self.menu.theme_opp
		else:
			self.editBarColor = LIGHTBLUE

	def createBar(self, difficulty, edit):
		self.diff = difficulty
		if not edit:
			self.edit = False
			diffBars = {"Easy": 100, "Medium": 85, "Hard": 70, "Expert": 60}
			self.barheight = self.menu.H * (70 / 740)
			if self.diff in diffBars:
				self.barheight = self.menu.H * (diffBars[difficulty]/740)
			self.bar = pygame.Surface([self.menu.W, self.barheight])
			self.bar_rect = self.bar.get_rect()
			self.bar_rect.x = 0
			self.bar_rect.y = self.menu.H*69/80 - self.barheight / 2

			self.whitebarheight = self.barheight*4/5
			self.whitebar = pygame.Surface([self.menu.W, self.whitebarheight])
			self.whitebar_rect = self.whitebar.get_rect()
			self.whitebar_rect.x = 0
			self.whitebar_rect.y = self.bar_rect.y + (self.barheight - self.whitebarheight) / 2
		else:
			# print("OKKKK")
			self.edit = True
			self.barheight = 2
			self.bar = pygame.Surface([self.menu.W, self.barheight])
			self.bar_rect = self.bar.get_rect()
			self.bar_rect.x = 0
			self.bar_rect.y = self.menu.H * 2/3

			self.whitebarheight = 0
			self.whitebar = pygame.Surface([self.menu.W, self.whitebarheight])
			self.whitebar_rect = self.whitebar.get_rect()
			self.whitebar_rect.x = 0
			self.whitebar_rect.y = self.menu.H * 2/3

	def playSong(self, name, type, difficulty, calibrating=False):
		self.song = Song(self.screen, self.menu, name, type,difficulty, calibrating)

	def drawSelf(self):
		barcolor = self.menu.theme_opp
		if self.edit: barcolor = self.editBarColor
		pygame.draw.rect(self.screen, barcolor, self.bar_rect)
		pygame.draw.rect(self.screen, self.menu.theme, self.whitebar_rect)

	def update(self, keys):

		if self.song:
			self.song.update(keys)
