from variables import *
from Song import *
from Player import *




class Menu:

	def __init__(self,screen, clock, dim):
		self.W = dim[0]
		self.H = dim[1]
		self.theme = BLACK
		self.theme_opp = WHITE
		self.theme_grey = GREY
		self.clock = clock
		self.done = False
		self.albumImage = None
		self.openhihatMode = True
		try:
			with open(fp + 'cache/Preferences.txt', 'rb') as rf:
				pref = pickle.load(rf)
				self.lag = pref["lag"]
		except:
			self.lag = 0

		self.topLeft = (self.W // 12, self.H / 10)
		self.topRight = (11 * self.W // 12, self.H / 10)
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
		self.sortBy = 0
		self.opaque = pygame.Surface((self.W,self.H))
		self.opaque.set_alpha(220)


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


		self.font = pygame.font.Font(fp + 'Assets/Fonts/UNI.otf', 40 * int(self.H / 740))
		self.bigfont = pygame.font.Font(fp + 'Assets/Fonts/Uni Sans Heavy.otf', 60* int(self.H / 740))

	def addText(self, text, color, center, big=False, bgcolor=None, align="center"):
		sub = None
		if "-" in text and text[0] != "-":
			sub = text.split("-")[0].strip()
			text = text.split("-")[1].strip()

		if big:
			txt = self.bigfont.render(text, True, color, bgcolor)
		else:
			txt = self.font.render(text, True, color, bgcolor)
		textRect = txt.get_rect()
		# textRect.right = 150
		if align == "right":
			textRect.topright = center
		elif align == "left":
			textRect.topleft = center
		else:
			textRect.center = center

		self.screen.blit(txt, textRect)
		if sub:
			subtxt = self.font.render(sub, True, color, bgcolor)
			subtextRect = subtxt.get_rect()
			if align == "right": subtextRect.topright = (center[0], center[1]+textRect.size[1]*0.85)
			if align == "center": subtextRect.center = center
			if align == "left": subtextRect.topleft = (center[0], center[1]+textRect.size[1]*0.85)

			# combtextRect = textRect.union(subtextRect)

			self.screen.blit(subtxt, subtextRect)
		return textRect


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
		songname = self.selected_Song.split("-")[1]
		if not self.record:
			# with open('cache/RecordedSongs.txt', 'rb') as rf:
			# 	recorded_songs = pickle.load(rf)
			with open(fp + 'cache/RecordedSongsJSON.json') as json_file:
			    recorded_songs = json.load(json_file)
			self.options = []
			if songname in recorded_songs:
				for d in possOptions:
					if d in recorded_songs[songname]:
						op = "{}%-{}".format(int(math.floor(100*recorded_songs[songname][d]["HighScore"])),d)
						self.options.append(op)
			if self.options == []: self.loadSongs()
		else:

			self.options = possOptions
			with open(fp + 'cache/RecordedSongsJSON.json') as json_file:
			    recorded_songs = json.load(json_file)
			if songname in recorded_songs:
				for d in possOptions:
					if d in recorded_songs[songname]:
						self.options[self.options.index(d)] = "Overwrite-" + str(d)

	def loadCalibrate(self):
		self.player.createBar("Hard")
		self.player.playSong("Dance Dance.mp3", type = "None", difficulty="Hard", calibrating=True)
		self.inGame = True

	def toggleSortBy(self):
		self.sortBy = 1 - self.sortBy
		self.selectedOption = 0
		self.loadSongs()

	def mySort(self,x):
		try:
			return x.split("-")[self.sortBy]
		except:
			try:
				return str(x,'utf-8').split("-")[self.sortBy]
			except:
				return str(x,'utf-8')

	def loadSongs(self):
		self.menuType = "Choose Song"
		directory = os.fsencode(fp + "Assets/Songs")
		self.options = []
		# self.selectedOption = 0
		if self.record: self.loadType = "Record"
		if self.load: self.loadType = "Load"
		if self.edit: self.loadType = "Edit"
		self.header = self.loadType
		if self.load:
			with open(fp + 'cache/RecordedSongsJSON.json') as json_file:
				recorded_songs = json.load(json_file)
		for file in sorted(os.listdir(directory),key=self.mySort):
			if "DS" not in str(file):
				artist = str(file,'utf-8').split("-")[0]
				songmp3 = str(file,'utf-8').split("-")[1]
				song = songmp3.replace(".mp3","")
				if self.load:
					if songmp3 in recorded_songs:
						self.options.append(str(file,'utf-8'))
				else:
					self.options.append(str(file,'utf-8'))
					if not os.path.exists(fp + "Assets/Albums/" + str(artist) + "-" + str(song) + ".jpg"):
						try:
							results = dc.search(song,artist=artist,type='master')[0]
							img_data = requests.get(results.images[0]["resource_url"]).content
							with open(fp + "Assets/Albums/" + str(file,'utf-8').replace(".mp3","") + ".jpg", 'wb') as handler:
							    handler.write(img_data)
						except:
							pass

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
		# i = 0
		if self.menuType == "Main":
			self.addText("Open Hi Hat: " + ("Yes" if self.openhihatMode else "No"),self.theme_opp,self.topRight,big=False,align="right")
		if self.menuType == "Choose Difficulty": self.addText(self.header,self.theme_opp,self.topLeft,big=True,align="left")
		# 	i += textRect.y + textRect.size[1]
		if self.albumImage and self.menuType == "Choose Difficulty":
			self.screen.blit(self.albumImage, (self.topLeft[0],3*(self.H / 10)))

		n = int(6 * self.H/740)
		if self.selectedOption <= n // 3:
			start = 0
			end = min((n - 1),len(self.options))
		elif self.selectedOption > n // 3:
			start = self.selectedOption - (n // 3) if (len(self.options) > (n // 3) and self.selectedOption < len(self.options) - (n // 2)) else max(0,len(self.options) - (n-1))
			end = min(self.selectedOption + (n // 2) + 1,len(self.options))

		i = 0
		options_i = start
		# print(start, end+1, self.selectedOption)
		for option in self.options[start:end+1]:
			txt = option.replace(".mp3","")
			yy = max((len(self.options) <= (2 * n // 3)) * ((3)*(self.H / 10)), (self.H / 10)) + ((i % n) )*125
			xx = self.W / 3
			if options_i  == self.selectedOption:
				if self.edit or self.selection == "Edit":
					textRect = self.addText(txt,BLACK,(xx, yy), big=True,bgcolor=LIGHTBLUE,align="left")
				else:
					textRect = self.addText(txt,BLACK,(xx, yy),big=True,bgcolor=YELLOW if not self.record else LIGHTRED,align="left")

				if self.albumImage and self.menuType == "Choose Song":
					ay = yy
					ay -= max(0, ay + self.albumImage.get_height() - self.H)
					self.screen.blit(self.albumImage, (self.topLeft[0],ay))

			else:
				color = GREY if ((i >= (n-1) and options_i < len(self.options)-1) or (i==0 and start > 0)) else self.theme_opp
				self.addText(txt,color,(xx, yy),big=True,align="left")
				text = self.font.render(txt, True, self.theme_opp)
			i += 1
			options_i += 1

	def toggleHiHatMode(self):
		self.openhihatMode = not self.openhihatMode

	def toggleDarkMode(self):
		if self.theme == WHITE:
			self.theme = BLACK
			self.theme_opp = WHITE
		else:
			self.theme = WHITE
			self.theme_opp = BLACK

	def addLag(self,i):
		self.lag += i



	def playPreview(self):
		self.albumImage = None
		try:
			self.albumImage = pygame.image.load(fp + "Assets/Albums/"+ str(self.options[self.selectedOption].replace("mp3","jpg"))).convert()
			self.albumImage = pygame.transform.scale(self.albumImage, (self.H//3, self.H//3))
		except:
			pass

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

		keys = pygame.key.get_pressed()
		for k in compKeys:
			if keys[k]: self.pressedKeys.append(allPads[k])
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True


		if self.joystick_count != 0:
			for i in controlPads:
				try:
					if self.my_joystick.get_button(i):
						self.pressedKeys.append(controlPads[i])
				except:
					pass

			for i in DPAD:
				if self.my_joystick.get_hat(0) == i:
					self.pressedKeys.append(allPads[i])

			if self.openhihatMode:
				closedHiHat = False
				for i in DPAD:
					if self.my_joystick.get_hat(0) == i:
						if i == (-1,0):
							closedHiHat = True
				if "hihat" in self.pressedKeys:
					if not closedHiHat:
						self.pressedKeys.append("openhihat")
						self.pressedKeys.remove("hihat")
					if closedHiHat:
						self.pressedKeys.remove("left")

		self.pressedKeys = list(set(self.pressedKeys))

		self.newPressedKeys = []
		for i in self.pressedKeys:
			if (i not in self.prevPressedKeys):
				self.newPressedKeys.append(i)

		self.newPressedKeys = list(set(self.newPressedKeys))



	def update(self):
		self.screen.fill(self.theme)

		self.updatePressed()
		# if self.newPressedKeys != []: print(self.newPressedKeys)
		if not self.inGame:
			self.loadMenu()
			# pressed = []

			if self.justReturned:
				if self.menuType == "Choose Difficulty":
					self.loadDifficulty()
				self.justReturned = False

			if inKeys(["home", "snare"], self.newPressedKeys):
				self.selectedOption = self.prevSelectionOption
				if self.menuType == "Main":
					self.toggleHiHatMode()
					# self.toggleDarkMode()
				if self.menuType == "Choose Song":
					self.selectedOption = [self.loadType in x for x in ["Load Song", "Record Song", "Edit"]].index(True)
					self.loadMain()
				elif self.menuType == "Choose Difficulty":
					self.loadSongs()
					# self.playPreview()
			if inKeys(["down", "tom"], self.newPressedKeys):
				self.selectedOption = (self.selectedOption + 1) % len(self.options)
				if self.menuType == "Choose Song": self.playPreview()
			if inKeys(["up", "hihat", "openhihat"], self.newPressedKeys):
				self.selectedOption = (self.selectedOption -1) % len(self.options)
				if self.menuType == "Choose Song": self.playPreview()
			self.selection = self.options[self.selectedOption] if self.selectedOption < len(self.options) else 0

			if self.menuType == "Main":
				self.edit = self.selection  == "Edit"
				self.record = self.selection  == "Record Song"

			if inKeys("kick", self.newPressedKeys):
				self.toggleSortBy()
			if inKeys("crash", self.newPressedKeys):
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
					diff = self.options[self.selectedOption].split("-")[1] if "-" in self.options[self.selectedOption] else self.options[self.selectedOption]
					self.player.createBar(diff, self.edit)
					self.player.playSong(self.selected_Song, type=self.loadType, difficulty=diff)
					self.inGame = True

		else:
			self.player.update()
