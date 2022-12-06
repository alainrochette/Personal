from variables import *
from Pad import *




class Song:
	def __init__(self,screen,menu,filename, type,difficulty, calibrating=False):
		self.menu = menu
		self.paused = False
		self.lag = self.menu.lag
		self.difficulty = difficulty
		self.vel = 1
		self.filename = filename
		self.name = filename.split("-")[1]
		self.artist = filename.split("-")[0]
		if self.name: self.vel = {"Easy":1, "Medium":1.1, "Hard":1.2, "Expert":1.3}[self.difficulty]
		self.vel = 1
		self.SONGLAG = self.menu.H * 1.4
		self.calibrating = calibrating
		self.missed = 0
		self.hits = 0
		self.t = 0
		self.streak = 0
		self.totalNotes = 0
		self.longestStreak = 0
		self.prevt = 0
		self.all_notes_list = pygame.sprite.Group()
		self.edit = False
		self.record = False
		self.free = False
		self.editSongT = 0
		self.editSongAccum = 0
		self.editting = False
		self.editSongPlaying = False
		self.lag_or_scroll = "Scroll"
		self.grabbed = None
		if type == "Edit":
			self.edit = True
		if type == "Load":
			self.free = True
		if type == "Record":
			self.record = True
		self.screen = screen
		self.recordedSong = []
		self.playing_song = False
		self.playing_song_t = 0
		self.playing_song_start_t = 0
		self.startRecord = -1
		self.scrollSpeed = 1
		self.prev = []
		self.wav = None
		self.songPlaying = False
		self.songEnded = False
		self.countDownEnded = False
		self.countDownEndedT = 0
		self.pauseCountDownStarted = False
		self.pauseCountDownT = 0
		self.startPausedT = 0
		self.totalPausedT = 0
		try:
			with open(fp + 'cache/RecordedSongsJSON.json') as json_file:
			    self.AllSongs = json.load(json_file)
			# with open('cache/RecordedSongs.txt', 'rb') as rf:
			# 	self.AllSongs = pickle.load(rf)
		except:
			self.AllSongs = None

		self.RecSong = None
		if self.name and not self.record:
			self.RecSong = self.AllSongs[self.name][self.difficulty]
			self.recordedSong = self.RecSong["Notes"]

			if "Lag" in self.RecSong: self.lag = self.RecSong["Lag"]
			self.recordedSong = [[l[0] + self.lag, l[1]] for l in self.recordedSong]
			self.startRecord = self.recordedSong[0][0]




		if filename:
			# self.wav = pygame.mixer.Sound("Assets/Songs/" + str(name))
			pygame.mixer.music.load(fp + "Assets/Songs/" + str(filename))
			# self.countdown = 3000
			self.startCountdownT = pygame.time.get_ticks()
			if self.edit:
				self.songPlaying = True
				self.editSongPlaying = True
				# pygame.mixer.music.stop()
				pygame.mixer.music.play()



	def toggleLagOrScroll(self):
		if self.lag_or_scroll == "Scroll":
			self.lag_or_scroll = "Lag"
		else:
			self.lag_or_scroll = "Scroll"


	def songStats(self, recording):
		if recording:
			notes = self.recordedSong
			if self.edit: notes = [[p[0] + self.lag, p[1]] for p in self.recordedSong]

			return {"Notes": notes,
					"HighScore": 0,
					"Hits": 0,
					"Streak": 0,
					"Lag": 0}
		if self.edit:
			notes = self.recordedSong
		else:
			notes = self.RecSong["Notes"]

		return {"Notes":notes,
				"HighScore": max(self.score,self.RecSong["HighScore"]),
				"Hits": max(self.hits,self.RecSong["Hits"]),
				"Streak": max(self.longestStreak,self.RecSong["Streak"]),
				"Lag": self.lag}

	def saveScore(self):
		self.longestStreak = max(self.streak,self.longestStreak)
		self.AllSongs[self.name][self.difficulty] = self.songStats(recording=False)

		with open(fp + "cache/RecordedSongsJSON.json", "w") as out_file:
			json.dump(self.AllSongs, out_file, indent = 4)

		out_file.close()

	def saveRecording(self, onlySaveLag=False):
		if len(self.recordedSong)>0:
			if onlySaveLag:
				self.AllSongs[self.name][self.difficulty]["Lag"] = self.lag
			else:
				if self.name not in self.AllSongs:
					self.AllSongs[self.name] = {self.difficulty: self.songStats(recording=True)}
				else:
					self.AllSongs[self.name][self.difficulty] = self.songStats(recording=True)

			with open(fp + "cache/RecordedSongsJSON.json", "w") as out_file:
				json.dump(self.AllSongs, out_file, indent = 4)

	def countdown(self):
		if not self.name:
			self.countDownEnded = True
			self.songPlaying = True
		if not self.songPlaying and not self.songEnded:
			if (pygame.time.get_ticks() - self.startCountdownT) > 3000 :
				self.countDownEnded = True
				if self.countDownEndedT == 0: self.countDownEndedT = pygame.time.get_ticks()
				if not self.record:
					if self.recordedSong != [] and self.recordedSong[0][0] < 0:
						self.startRecord = -1*self.recordedSong[0][0]
						for i in range(len(self.recordedSong)):
							self.recordedSong[i][0] += self.startRecord
					else:
						if self.startRecord == -1:
							self.songPlaying = True
							pygame.mixer.music.stop()
							pygame.mixer.music.play()
							self.playing_song_start_t = pygame.time.get_ticks()
						elif (pygame.time.get_ticks() - self.countDownEndedT ) > (self.SONGLAG / (self.menu.clock.get_fps() / 100)) :
							self.songPlaying = True
							pygame.mixer.music.stop()
							pygame.mixer.music.play()
							self.playing_song_start_t = pygame.time.get_ticks()

				else:
					self.songPlaying = True
					pygame.mixer.music.stop()
					pygame.mixer.music.play()
					self.countDownEndedT = pygame.time.get_ticks()
					self.playing_song_start_t = pygame.time.get_ticks()
			else:
				self.showStats()
				CDtext = str(int(math.ceil(3 - ((pygame.time.get_ticks() - self.startCountdownT) / 1000))))
				self.menu.addText(CDtext,self.menu.theme_opp,(self.menu.topLeft[0],self.menu.H*0.7),big=True)

	def formatScore(self,frac=None,total=False):
		if total:
			num = self.totalNotes
			den = len(self.RecSong["Notes"])
		else:
			den = self.hits + self.missed
			num = self.hits
		if frac:
			num, den = frac[0], frac[1]
		perc = "0%"
		if den != 0:
			perc = str(int(math.floor(100*num/den))) + "%"
		return perc

	def addLag(self, n):
		self.lag += n
		self.menu.addLag(n)

	def showStats(self):

		          # this fills the entire surface
		self.menu.opaque.fill(self.menu.theme)
		self.screen.blit(self.menu.opaque, (0,0))


		perc = self.formatScore()
		txt = str(self.hits) + " / " + str(self.hits + self.missed)



		if not self.record and self.name:
			textRect = self.menu.addText(self.filename.replace(".mp3",""),self.menu.theme_opp,self.menu.topLeft,big=True, align="left")
			self.menu.addText(self.difficulty.upper(),self.menu.theme_opp,(self.menu.topLeft[0],self.menu.topLeft[1]+self.menu.H*0.12),big=False, align = "left")
			if self.menu.albumImage:
				self.screen.blit(self.menu.albumImage, (self.menu.topLeft[0],3*(self.menu.H / 10)))

			# if "HighScore" in self.RecSong:
			if not self.paused and (self.countDownEnded or self.songEnded):
				self.menu.addText(perc,self.menu.theme_opp,(self.menu.topLeft[0], 0.8* self.menu.H),big=True,  align="left")
				self.menu.addText(str(self.longestStreak) + " streak",self.menu.theme_opp,(self.menu.topLeft[0], 0.85* self.menu.H),  align="left")

				if self.score > self.RecSong["HighScore"]:
					self.menu.addText("New Highscore!",self.menu.theme_opp,(self.menu.W / 3, 3*(self.menu.H / 10)+ 1*125),big=True, align="left")
				else:
					self.menu.addText("Highscore: " + str(self.formatScore([self.RecSong["Hits"],len(self.RecSong["Notes"])])),self.menu.theme_opp,(self.menu.W / 3, 3*(self.menu.H / 10)+ 1*125), align="left")
				if self.longestStreak > self.RecSong["Streak"]:
					self.menu.addText("New Longest Streak!",self.menu.theme_opp,(self.menu.W / 3, 3*(self.menu.H / 10)+ 2*125),big=True, align="left")
				else:
					self.menu.addText("Longest Streak: " + str(self.RecSong["Streak"]),self.menu.theme_opp,(self.menu.W / 3, 3*(self.menu.H / 10)+ 2*125), align="left")
			elif self.paused:
				# self.menu.addText("Paused",self.menu.theme_opp,(0.5*self.menu.W, 0.6* self.menu.H),big=True)

				self.menu.addText(self.formatScore(total=True) + " Finished",self.menu.theme_opp,(self.menu.topLeft[0], 0.8* self.menu.H),big=True, align="left")

				self.menu.addText("Crash to Resume",self.menu.theme_opp,(self.menu.topLeft[0], 0.85* self.menu.H),big=False, align="left")

			if self.songEnded:
				if inKeys("home", self.menu.newPressedKeys):
					if self.record: self.saveRecording()
					self.menu.returnToMenu()
					return


	def updateStats(self):
		if not self.edit:
			self.score = self.hits / (self.hits + self.missed) if (self.hits + self.missed) > 0 else 0

			if self.hits + self.missed == 0:
				perc = "0%"
				txt = str(self.hits) + " / " + str(self.hits + self.missed)
			else:
				perc = str(int(math.floor(100*self.hits/(self.hits + self.missed)))) + "%"
				txt = str(self.hits) + " / " + str(self.hits + self.missed)

			self.menu.addText(perc,self.menu.theme_opp,(0.9*self.menu.W, 0.1* self.menu.H),big=True)
			self.menu.addText(txt,self.menu.theme_opp,(0.9*self.menu.W, 0.16* self.menu.H))

		if not self.record and self.name and not self.paused:
			if self.edit:
				self.menu.addText(self.lag_or_scroll,self.menu.theme_opp,(0.07*self.menu.W, 0.02*self.menu.H ),big=False)

			self.menu.addText("+",self.menu.theme_opp,(0.07*self.menu.W, 0.08*self.menu.H ),big=False)
			if self.lag != 0: self.menu.addText(str(self.lag),self.menu.theme_opp,(0.07*self.menu.W, 0.13* self.menu.H),big=False)
			self.menu.addText("-",self.menu.theme_opp,(0.07*self.menu.W, 0.18*self.menu.H),big=False)
			# self.menu.addText("lag",self.menu.theme_opp,(1250, H - 100))


		if self.edit:
			self.menu.addText(str(round(self.editSongT/1000,1)),self.menu.theme_opp,(0.05*self.menu.W,self.menu.player.bar_rect.y - 0.03*self.menu.H))


	def updateCountdownPause(self):
		self.pauseCountDownStarted = True
		if self.pauseCountDownT == 0: self.pauseCountDownT = pygame.time.get_ticks()
		if (pygame.time.get_ticks() - self.pauseCountDownT) > 3000:
			pygame.mixer.music.unpause()
			self.pauseCountDownStarted = False
			self.totalPausedT += (pygame.time.get_ticks() - self.startPausedT)
			self.startPausedT = 0
			self.pauseCountDownT = 0
			self.updatePlay()

		else:
			# self.menu.opaque.fill(self.menu.theme)
			# self.screen.blit(self.menu.opaque, (0,0))
			CDtext = str(int(math.ceil(3 - ((pygame.time.get_ticks() - self.pauseCountDownT) / 1000))))
			self.menu.addText(CDtext,self.menu.theme_opp,(self.menu.topLeft[0],self.menu.H*0.7),big=True)


	def updatePause(self):
		if not self.pauseCountDownStarted:
			if self.startPausedT == 0: self.startPausedT = pygame.time.get_ticks()
			self.showStats()

			if self.paused and inKeys("crash", self.menu.newPressedKeys):
				self.paused = False
				self.updateCountdownPause()
			if inKeys("home", self.menu.newPressedKeys):
				if self.record:
					self.saveRecording()
				else:
					self.saveRecording(onlySaveLag=True)
				self.menu.returnToMenu()
				return
		else:
			self.updateCountdownPause()



	def updatePlay(self):
		if self.playing_song_start_t == 0: self.countdown()
		if self.songEnded and not self.record: self.showStats()
		if self.countDownEnded and not self.songEnded:
			if not self.paused: self.menu.player.drawSelf()
			self.updateStats()
			if not self.pauseCountDownStarted and not self.paused:
				self.all_notes_list.update()

			# self.all_notes_list.draw(self.screen)
			for n in self.all_notes_list:
				n.drawSelf(self.screen)
			# self.all_notes_list.draw(self.screen)
			if not self.paused:
				if self.free and self.name and not self.pauseCountDownStarted:
					if inKeys("down", self.menu.newPressedKeys):
						self.addLag(-25)
						self.recordedSong = [[l[0] - 25, l[1]] for l in self.recordedSong]
					if inKeys("up", self.menu.newPressedKeys):

						self.addLag(25)
						self.recordedSong = [[l[0] + 25, l[1]] for l in self.recordedSong]

					t = pygame.time.get_ticks() - self.countDownEndedT - self.totalPausedT
					if self.recordedSong:
						if abs(self.recordedSong[0][0] - t) < 30:

							self.addPad(self.recordedSong[0][0],controlPads[self.recordedSong[0][1]])
							self.recordedSong = self.recordedSong[1:]

					if len(self.recordedSong) == 0 and len(self.all_notes_list.sprites()) == 0:
						self.playing_song = False
						self.recordedSong = []

						if not pygame.mixer.music.get_busy():
							self.saveScore()
							self.songEnded = True

					if inKeys("home", self.menu.newPressedKeys):
						if len(self.recordedSong) == 0:
							self.saveScore()
							self.songEnded = True
						else:
							self.paused = True
						pygame.mixer.music.pause()
						return

					for i in self.menu.newPressedKeys:
						i_played = False
						for note in self.all_notes_list:
							if note.padtype == i:
								if note.rect.colliderect(self.menu.player.bar_rect) and not note.played:
									note.played = True
									i_played = True
									continue
						if not i_played:
							if i in drumControls:
								self.addPad(t=0,type=i,missed=True)
								self.missed += 1

				else:
					# if self.menu.joystick_count != 0 :
					if inKeys("home", self.menu.newPressedKeys):
						if self.record:
							self.saveRecording()
							self.menu.returnToMenu()
							return
					for i in self.menu.newPressedKeys:
						if inKeys(i, drumControls):
							if self.record:
								self.recordedSong.append([pygame.time.get_ticks()-self.countDownEndedT,padControls[i]])
							self.addPad(pygame.time.get_ticks()-self.countDownEndedT,i)

		if self.paused: self.updatePause()
		if self.pauseCountDownStarted: self.updateCountdownPause()

	def toggleEditPlay(self):
		if self.editSongPlaying:
			pygame.mixer.music.pause()
			# self.editSongT = pygame.mixer.music.get_pos()
			self.editSongAccum = self.editSongT
		else:
			# pygame.mixer.music.stop()
			# pygame.mixer.music.set_pos(self.editSongT)
			pygame.mixer.music.play(start=(self.editSongAccum)/1000)
			# pygame.mixer.music.unpause()
		self.editSongPlaying = not self.editSongPlaying

	def toggleEdit(self):

		self.menu.player.toggleEdit()
		self.editting = not self.editting

	def addPad(self, t, type, editadd=False, missed=False):
		self.all_notes_list.add(Pad(self,t,type, self.record, sound=False, missed=missed))
		if self.edit and editadd:
			for p in self.recordedSong:
				if t - self.lag < p[0]:
					self.recordedSong.insert(self.recordedSong.index(p), [t- self.lag, padControls[type]])
					return
			self.recordedSong.append([t - self.lag, padControls[type]])
			return

	def editSelectPad(self):
		self.grabbed = False
		miny = 1000000
		minp = None
		for p in self.all_notes_list:
			if abs(p.rect.y - self.menu.player.bar_rect.y) < miny:
				minp = p
				miny = abs(p.rect.y - self.menu.player.bar_rect.y)
		if minp:

			minp.toggleGrab()
			self.grabbed = minp

	def removeSelectedPad(self):
		for p in self.recordedSong:
			if p[0] + self.lag == self.grabbed.t:
				self.recordedSong.remove(p)
				self.addEditPads(update=True)
				self.grabbed = False
				return

	def addEditPads(self, update=False):
		if self.editSongPlaying or update:
			self.all_notes_list.empty()
			ht = self.SONGLAG / (self.menu.clock.get_fps() / 100)
			for p in self.recordedSong:
				if p[0] - self.editSongT<= ht*(2/3) and p[0] - self.editSongT > -1*(ht*(1/3)):
					self.addPad(p[0] + self.lag ,controlPads[p[1]])

	def updateEdit(self):
		self.updateStats()
		self.addEditPads()
		self.menu.player.drawSelf()
		self.all_notes_list.update()

		for n in self.all_notes_list:
			n.drawSelf(self.screen)
		# self.all_notes_list.draw(self.screen)


		if self.editSongPlaying:
			self.editSongT = self.editSongAccum + pygame.mixer.music.get_pos()


		if inKeys("home", self.menu.newPressedKeys):
			self.saveRecording()
			self.menu.returnToMenu()
			return
		if inKeys("start", self.menu.newPressedKeys):
			self.toggleEditPlay()
		if inKeys("select", self.menu.newPressedKeys):
			self.editSelectPad()

		if inKeys("up", self.menu.pressedKeys):
			if self.lag_or_scroll == "Lag" and inKeys("up", self.menu.newPressedKeys):
				self.addLag(-25)
				self.addEditPads(update=True)
			elif self.lag_or_scroll == "Scroll":
				self.scrollSpeed = min(8, self.scrollSpeed * 1.01) if "up" in self.menu.prevPressedKeys else 1

				self.editSongAccum += 5 * self.scrollSpeed
				self.editSongT = self.editSongAccum
				self.addEditPads(update=True)
		if inKeys("down", self.menu.pressedKeys):
			if self.lag_or_scroll == "Lag" and inKeys("down", self.menu.newPressedKeys):
				self.addLag(25)
				self.addEditPads(update=True)
			elif self.lag_or_scroll == "Scroll":
				self.scrollSpeed = min(8, self.scrollSpeed * 1.01) if "down" in self.menu.prevPressedKeys else 1
				if self.editSongAccum - 5 * self.scrollSpeed > 0:
					self.editSongAccum -= 5 * self.scrollSpeed
					self.editSongT = self.editSongAccum
					self.addEditPads(update=True)

		if inKeys("right", self.menu.newPressedKeys) or inKeys("left", self.menu.newPressedKeys):
			self.toggleLagOrScroll()

		if self.grabbed:
			if "snare" in self.menu.newPressedKeys: self.removeSelectedPad()
		else:
			for i in self.menu.newPressedKeys:
				if inKeys(i, drumControls):
					self.addPad(self.editSongT,i, editadd=True)

	def update(self):
		if self.free or self.record:
			self.updatePlay()
		if self.edit:
			self.updateEdit()
