from variables import *
from Song import *
from Player import *




class Menu:

	def __init__(self,screen, clock, dim):
		self.W = dim[0]
		self.H = dim[1]
		self.theme = BLACK
		self.theme_opp = WHITE
		self.clock = clock
		self.done = False
		try:
			with open(fp + 'cache/Preferences.txt', 'rb') as rf:
				pref = pickle.load(rf)
				self.lag = pref["lag"]
		except:
			self.lag = 0
		self.lag = 0
		self.player = Player(screen, self)
		self.screen = screen
		self.loadMain()
		self.edit = False
		self.record = False
		self.load = False
		self.selectedOption = 0
		self.prevSelectionOption = 0
		self.inGame = False
		self.selected_Song = None
		self.prev = []
		self.loadType = "Main Menu"
		self.selection = ""
		self.justReturned = False
		self.previewTime = 0

		self.opaque = pygame.Surface((self.W,self.H))
		self.opaque.set_alpha(180)


		self.newPressedKeys = []
		self.prevPressedKeys = []
		self.pressedKeys = []
		# Count the joysticks the computer has
		self.my_joystick = None
		self.joystick_count = pygame.joystick.get_count()

		if self.joystick_count == 0:
			pass
		else:
			self.my_joystick = pygame.joystick.Joystick(0)
			self.my_joystick.init()


		self.font = pygame.font.Font(fp + 'Assets/Fonts/UNI.otf', 35 * int(self.H / 740))
		self.bigfont = pygame.font.Font(fp + 'Assets/Fonts/Uni Sans Heavy.otf', 60* int(self.H / 740))

	def addText(self, text, color, center,big=False):
		if big:
			txt = self.bigfont.render(text, True, color)
		else:
			txt = self.font.render(text, True, color)
		textRect = txt.get_rect()
		textRect.center = center
		self.screen.blit(txt, textRect)

	def returnToMenu(self):
		self.justReturned = True
		self.inGame = False
		pygame.mixer.music.stop()

	def loadDifficulty(self):
		pygame.mixer.music.stop()
		self.menuType = "Choose Difficulty"
		# self.selectedOption = 0
		possOptions = ["Easy", "Medium", "Hard", "Expert"]
		self.header = self.selected_Song.replace(".mp3","")
		if not self.record:
			# with open('cache/RecordedSongs.txt', 'rb') as rf:
			# 	recorded_songs = pickle.load(rf)
			with open(fp + 'cache/RecordedSongsJSON.json') as json_file:
			    recorded_songs = json.load(json_file)
			self.options = []
			if self.selected_Song in recorded_songs:
				for d in possOptions:
					if d in recorded_songs[self.selected_Song]:
						op = "{} - {}%".format(d, int(math.floor(100*recorded_songs[self.selected_Song][d]["HighScore"])))
						self.options.append(op)
			if self.options == []: self.loadSongs()
		else:

			self.options = possOptions

			with open(fp + 'cache/RecordedSongsJSON.json') as json_file:
			    recorded_songs = json.load(json_file)
			if self.selected_Song in recorded_songs:
				for d in possOptions:
					if d in recorded_songs[self.selected_Song]:
						self.options[self.options.index(d)] = str(d) + " - Overwrite"

	def loadCalibrate(self):
		self.player.createBar("Hard")
		self.player.playSong("Dance Dance.mp3", type = "None", difficulty="Hard", calibrating=True)
		self.inGame = True

	def loadSongs(self):
		self.menuType = "Choose Song"
		directory = os.fsencode(fp + "Assets/Songs")
		self.options = []
		# self.selectedOption = 0
		if self.record: self.loadType = "Record"
		if self.load: self.loadType = "Load"
		if self.edit: self.loadType = "Edit"
		self.header = self.loadType
		for file in os.listdir(directory):
			if "DS" not in str(file):
				self.options.append(str(file,'utf-8'))
		self.playPreview()

	def loadMain(self):
		pygame.mixer.music.stop()
		self.record = False
		self.menuType = "Main"
		self.loadType = "Main Menu"
		self.header = self.loadType
		self.options = ["Load Song", "Record Song", "Edit"]

	def loadMenu(self):
		if (pygame.time.get_ticks() - self.previewTime)/1000 >= 7:
			pygame.mixer.music.fadeout(2000)
		self.addText(self.header,self.theme_opp,(self.W // 2, self.H // 12),big=True)
		if self.menuType != "Main":
			self.addText(self.menuType,self.theme_opp,(self.W // 2, self.H // 7))

		i = 0
		for option in self.options:
			txt = option.replace(".mp3","")
			if i  == self.selectedOption:
				if self.edit or self.selection == "Edit":
					text = self.font.render(txt, True, BLACK, LIGHTBLUE)
				else:
					text = self.font.render(txt, True, BLACK, YELLOW if not self.record else LIGHTRED)
			else:
				text = self.font.render(txt, True, self.theme_opp)
			textRect = text.get_rect()

			xx = self.W*(((i)//5)+1) / (((len(self.options) - 1) // 5) + 2)
			yy = (self.H // 5) + ((i % 5) + 1)*100
			textRect.center = (xx, yy)
			i += 1
			self.screen.blit(text, textRect)

	def toggleDarkMode(self):
		if self.theme == WHITE:
			self.theme = BLACK
			self.theme_opp = WHITE
		else:
			self.theme = WHITE
			self.theme_opp = BLACK

	def addLag(self,i):
		self.lag += i



	# def run_scheduled_task(self):
	#     timer = th.Timer(1, pygame.mixer.music.play, [0,20,2000])
	#     timer.start()

	def playPreview(self):

		pygame.mixer.music.stop()
		self.previewTime = pygame.time.get_ticks()

		pygame.mixer.music.load(fp + "Assets/Songs/" + str(self.options[self.selectedOption]))
		# self.run_scheduled_task()
		try:
			pygame.mixer.music.play(start=20,fade_ms=4000)
		except:
			pygame.mixer.music.play(start=0,fade_ms=4000)

	def updatePressed(self):
		self.prevPressedKeys = self.pressedKeys
		self.pressedKeys = []

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key in allPads:
				self.pressedKeys.append(event.key)
			# if event.type == pygame.KEYUP:
			# 	self.prev = []

		if self.joystick_count != 0:
			for i in controlPads:
				if self.my_joystick.get_button(i):
					self.pressedKeys.append(controlPads[i])

		self.newPressedKeys = []
		for i in pressed:
			if (i not in self.prev):
				self.newPressedKeys.append(allPads[i])

	def update(self):
		self.screen.fill(self.theme)

		self.updatePressed()

		keys = []
		if self.inGame:
			if pygame.key.get_pressed()[pygame.K_DOWN]:
				keys.append(pygame.K_DOWN)
			elif pygame.key.get_pressed()[pygame.K_UP]:
				keys.append(pygame.K_UP)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				keys.append(event.key)
			if event.type == pygame.KEYUP:
				self.prev = []

		if not self.inGame:
			self.loadMenu()
			pressed = []

			if self.joystick_count != 0:
				for i in controlPads:
					if self.my_joystick.get_button(i):
						pressed.append(i)

			if self.justReturned:
				if self.menuType == "Choose Difficulty":
					self.loadDifficulty()
				if len(pressed) > 0:
					pressed = []
				else:
					self.justReturned = False
			pressed += keys
			newprev = []

			for i in pressed:
				if (i not in self.prev):
					if (i == 12) or (i == 2) or i == pygame.K_BACKSPACE:
						self.selectedOption = self.prevSelectionOption
						if self.menuType == "Main":
							self.toggleDarkMode()
						if self.menuType == "Choose Song":
							self.selectedOption = [self.loadType in x for x in ["Load Song", "Record Song", "Edit"]].index(True)
							self.loadMain()
						elif self.menuType == "Choose Difficulty":
							self.loadSongs()
							# self.playPreview()
					if i == 0 or i == pygame.K_DOWN:
						self.selectedOption = (self.selectedOption + 1) % len(self.options)
						if self.menuType == "Choose Song": self.playPreview()
					if i == 3 or i == pygame.K_UP:
						self.selectedOption = (self.selectedOption -1) % len(self.options)
						if self.menuType == "Choose Song": self.playPreview()
					self.selection = self.options[self.selectedOption]

					if self.menuType == "Main": self.edit = self.selection  == "Edit"
					if self.menuType == "Main": self.record = self.selection  == "Record Song"

					if i == 1 or i == pygame.K_RETURN:
						self.prevSelectionOption = self.selectedOption
						if self.menuType == "Main":
							if self.selection == "Edit":
								self.loadSongs()
								self.selectedOption = 0
							elif self.selection == "Load Song" or self.selection == "Record Song":
								self.edit = False
								self.record =  self.selection == "Record Song"
								self.load =  self.selection == "Load Song"

								self.loadSongs()
								self.selectedOption = 0
								# self.playPreview()
							elif self.selection == "Calibrate":
								self.loadCalibrate()

						elif self.menuType == "Choose Song":
							self.selected_Song = self.options[self.selectedOption]
							self.loadDifficulty()
							self.selectedOption = 0
						elif self.menuType == "Choose Difficulty":
							diff = self.options[self.selectedOption].split(" - ")[0]
							self.player.createBar(diff, self.edit)
							self.player.playSong(self.selected_Song, type=self.loadType, difficulty=diff)
							self.inGame = True
				newprev.append(i)

			self.prev = newprev

		else:
			self.player.update(keys)
