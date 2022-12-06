from variables import *
from Pad import *




class Song:
	def __init__(self,screen,menu,name, type,difficulty, calibrating=False):
		self.menu = menu
		self.paused = False
		self.keys = []
		# self.menu.lag = 0
		self.difficulty = difficulty
		self.vel = 1
		if name: self.vel = {"Easy":1, "Medium":1.1, "Hard":1.2, "Expert":1.3}[self.difficulty]
		self.vel = 1
		self.SONGLAG = self.menu.H * 1.4 / self.vel
		self.calibrating = calibrating
		self.missed = 0
		self.hits = 0
		self.t = 0
		self.streak = 0
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
		self.name = name
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

			self.recordedSong = [[l[0] + self.menu.lag, l[1]] for l in self.recordedSong]
			self.startRecord = self.recordedSong[0][0]





		if name:
			# self.wav = pygame.mixer.Sound("Assets/Songs/" + str(name))
			pygame.mixer.music.load(fp + "Assets/Songs/" + str(name))
			# self.countdown = 3000
			self.startCountdownT = pygame.time.get_ticks()
			if self.edit:
				self.songPlaying = True
				self.editSongPlaying = True
				# pygame.mixer.music.stop()
				pygame.mixer.music.play()

	def songStats(self, recording):
		if recording:
			return {"Notes": self.recordedSong,
					"HighScore": 0,
					"Hits": 0,
					"Streak": 0}
		if self.edit:
			notes = self.recordedSong
		else:
			notes = self.RecSong["Notes"]

		return {"Notes":notes,
				"HighScore": max(self.score,self.RecSong["HighScore"]),
				"Hits": max(self.hits,self.RecSong["Hits"]),
				"Streak": max(self.longestStreak,self.RecSong["Streak"])}

	def saveScore(self):
		self.longestStreak = max(self.streak,self.longestStreak)
		self.AllSongs[self.name][self.difficulty] = self.songStats(recording=False)

		with open(fp + "cache/RecordedSongsJSON.json", "w") as out_file:
			json.dump(self.AllSongs, out_file, indent = 4)

		out_file.close()

	def saveRecording(self):
		if len(self.recordedSong)>0:

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
						elif (pygame.time.get_ticks() - self.countDownEndedT ) > self.SONGLAG / (self.menu.clock.get_fps() / 100):
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
				self.menu.addText(CDtext,self.menu.theme_opp,(self.menu.W // 2, self.menu.H // 5 + 100),big=True)

	def formatScore(self,frac=None,total=False):
		if total:
			num = self.hits + self.missed
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

	def showStats(self):

		          # this fills the entire surface
		self.menu.opaque.fill(self.menu.theme)
		self.screen.blit(self.menu.opaque, (0,0))


		perc = self.formatScore()
		txt = str(self.hits) + " / " + str(self.hits + self.missed)

		if not self.record and self.name:
			self.menu.addText(self.name.replace(".mp3",""),self.menu.theme_opp,(0.5*self.menu.W, 0.15* self.menu.H),big=True)
			self.menu.addText(self.difficulty,self.menu.theme_opp,(0.5*self.menu.W, 0.2* self.menu.H))


			# if "HighScore" in self.RecSong:
			if not self.paused and self.countDownEnded:
				self.menu.addText(perc,self.menu.theme_opp,(0.5*self.menu.W, 0.3* self.menu.H),big=True)
				self.menu.addText(str(self.longestStreak) + " streak",self.menu.theme_opp,(0.5*self.menu.W, 0.35* self.menu.H))

				if self.score > self.RecSong["HighScore"]:
					self.menu.addText("New Highscore!",self.menu.theme_opp,(0.5*self.menu.W, 0.6* self.menu.H),big=True)
				else:
					self.menu.addText("Highscore: " + str(self.formatScore([self.RecSong["Hits"],len(self.RecSong["Notes"])])),self.menu.theme_opp,(0.5*self.menu.W, 0.6* self.menu.H))
				if self.longestStreak > self.RecSong["Streak"]:
					self.menu.addText("New Longest Streak!",self.menu.theme_opp,(0.5*self.menu.W, 0.7* self.menu.H),big=True)
				else:
					self.menu.addText("Longest Streak: " + str(self.RecSong["Streak"]),self.menu.theme_opp,(0.5*self.menu.W, 0.7* self.menu.H))
			elif self.paused:
				self.menu.addText("Paused",self.menu.theme_opp,(0.5*self.menu.W, 0.6* self.menu.H),big=True)

				self.menu.addText(self.formatScore(total=True) + " Finished",self.menu.theme_opp,(0.5*self.menu.W, 0.65* self.menu.H),big=False)

				self.menu.addText("Crash to Resume",self.menu.theme_opp,(0.5*self.menu.W, 0.9* self.menu.H),big=False)

			if self.songEnded:
				newprev = []

				for i in allPads:
					if (self.menu.my_joystick and i in controlPads and self.menu.my_joystick.get_button(i) or
						i in self.keys):
						if i not in self.prev:
							if (i == 12) or i == pygame.K_BACKSPACE:
								if self.record: self.saveRecording()
								self.menu.returnToMenu()
								return
						newprev.append(i)
				self.prev = newprev
				# self.menu.addText(str(self.longestStreak) + " streak",self.menu.theme_opp,(0.5*self.menu.W, 0.35* self.menu.H))

			# else:
			# 	self.menu.addText("New Highscore!",self.menu.theme_opp,(0.5*self.menu.W, 0.7* self.menu.H),big=True)
			# 	self.menu.addText("New Longest Streak!",self.menu.theme_opp,(0.5*self.menu.W, 0.8* self.menu.H),big=True)

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

		if not self.record and self.name:
			self.menu.addText("+",self.menu.theme_opp,(0.07*self.menu.W, 0.08*self.menu.H ),big=False)
			if self.menu.lag != 0: self.menu.addText(str(self.menu.lag),self.menu.theme_opp,(0.07*self.menu.W, 0.13* self.menu.H),big=False)
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
			self.updatePlay(self.keys)

		else:
			CDtext = str(int(math.ceil(3 - ((pygame.time.get_ticks() - self.pauseCountDownT) / 1000))))
			self.menu.addText(CDtext,self.menu.theme_opp,(self.menu.W // 2, self.menu.H // 5 + 100),big=True)


	def updatePause(self):
		if not self.pauseCountDownStarted:
			if self.startPausedT == 0: self.startPausedT = pygame.time.get_ticks()
			self.showStats()
			newprev = []
			for i in allPads:
				if (self.menu.my_joystick and i in controlPads and self.menu.my_joystick.get_button(i) or
					i in self.keys):
					if i not in self.prev:
						if self.paused and allPads[i] == "crash":
							self.paused = False
							self.updateCountdownPause()

						if (i == 12) or i == pygame.K_BACKSPACE:
							if self.record: self.saveRecording()
							self.menu.returnToMenu()
							return

					newprev.append(i)
			self.prev = newprev
		else:
			self.updateCountdownPause()



	def updatePlay(self, keys):
		self.keys = keys
		if self.playing_song_start_t == 0: self.countdown()
		if self.songEnded and not self.record: self.showStats()
		if self.countDownEnded and not self.songEnded:
			if not self.paused: self.menu.player.drawSelf()
			self.updateStats()
			if not self.pauseCountDownStarted and not self.paused:
				self.all_notes_list.update()
			self.all_notes_list.draw(self.screen)
			if not self.paused:
				if self.free and self.name and not self.pauseCountDownStarted:
					pressed_pad = None
					for i in allPads:
						if ((self.menu.my_joystick and self.menu.my_joystick.get_hat(0) == i) or
							i in keys):
							if i not in self.prev:
								if allPads[i] == "down":
									self.menu.addLag(-25)
									self.recordedSong = [[l[0] - 25, l[1]] for l in self.recordedSong]
								elif allPads[i] == "up":
									self.menu.addLag(25)
									self.recordedSong = [[l[0] + 25, l[1]] for l in self.recordedSong]
							pressed_pad = i


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


					newprev = []
					if pressed_pad: newprev.append(pressed_pad)
					for i in allPads:
						if (self.menu.my_joystick and i in controlPads and self.menu.my_joystick.get_button(i) or
							i in self.keys):
							if i not in self.prev:


								if (i == 12) or i == pygame.K_BACKSPACE:
									self.paused = True
									pygame.mixer.music.pause()
									# return


								got_one = False
								for note in self.all_notes_list:
									if note.padtype == allPads[i]:
										if note.rect.colliderect(self.menu.player.bar_rect):
											note.played = True
											got_one = True
								if not got_one and (i in drumKeys or i in drumPads):
									self.addPad(t=0,type=allPads[i],missed=True)
									self.missed += 1
								# if self.calibrating:
								# 	if i == 3:
								# 		self.menu.addLag(-25)
								# 		self.recordedSong = [[l[0] - 25, l[1]] for l in self.recordedSong]
								# 	if i == 0:
								# 		self.menu.addLag(25)
								# 		self.recordedSong = [[l[0] + 25, l[1]] for l in self.recordedSong]

							newprev.append(i)
					self.prev = newprev

				else:
					# if self.menu.joystick_count != 0 :
						pressed = []
						for i in allPads:
							if self.menu.my_joystick and i in controlPads and self.menu.my_joystick.get_button(i):
								pressed.append(i)
						pressed += keys
						newprev = []
						for i in pressed:
							if (i == 12) or i == pygame.K_BACKSPACE :
								if self.record: self.saveRecording()
								self.menu.returnToMenu()
								return
							if (i not in self.prev) and (i in controlPads or (not self.menu.my_joystick and i in drumKeys)):
								if self.record:
									self.recordedSong.append([pygame.time.get_ticks()-self.countDownEndedT,padControls[allPads[i]]])
									# self.song.recordedSong[pygame.time.get_ticks()] = i

								self.addPad(pygame.time.get_ticks()-self.countDownEndedT,allPads[i])


							newprev.append(i)

						self.prev = newprev
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
				if t - self.menu.lag < p[0]:
					self.recordedSong.insert(self.recordedSong.index(p), [t- self.menu.lag, padControls[type]])
					return
			self.recordedSong.append([t - self.menu.lag, padControls[type]])
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
			if p[0] + self.menu.lag == self.grabbed.t:
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
					self.addPad(p[0] + self.menu.lag ,controlPads[p[1]])

	def updateEdit(self, keys):
		self.updateStats()
		self.addEditPads()
		self.menu.player.drawSelf()
		self.all_notes_list.update()
		self.all_notes_list.draw(self.screen)


		if self.editSongPlaying:
			self.editSongT = self.editSongAccum + pygame.mixer.music.get_pos()

		newprev = []
		for i in allPads:
			# if self.menu.joystick_count != 0:
			if ((self.menu.my_joystick and isinstance(i, int) and self.menu.my_joystick.get_button(i)) or
				self.menu.my_joystick and self.menu.my_joystick.get_hat(0) == i or
				i in keys):
				if i not in self.prev or i in DPAD or i == pygame.K_DOWN or i == pygame.K_UP:
					if (i == 12) or (not self.menu.my_joystick and i == pygame.K_BACKSPACE):
						self.saveRecording()
						self.menu.returnToMenu()
						return
					if (allPads[i] == "start"):
						self.toggleEditPlay()
					if (allPads[i] == "select"):
						self.editSelectPad()
					if (allPads[i] == "left"):
						self.menu.addLag(-25)
						self.addEditPads(update=True)
					if (allPads[i] == "right"):
						self.menu.addLag(25)
						self.addEditPads(update=True)
					if not self.editSongPlaying:
						if (allPads[i] == "up"):
							self.scrollSpeed = min(8, self.scrollSpeed * 1.01) if i in self.prev else 1
							self.editSongAccum += 5 * self.scrollSpeed
							self.editSongT = self.editSongAccum
							self.addEditPads(update=True)
						if (allPads[i] == "down"):
							self.scrollSpeed = min(8, self.scrollSpeed * 1.01) if i in self.prev else 1
							self.editSongAccum -= 5 * self.scrollSpeed
							self.editSongT = self.editSongAccum
							self.addEditPads(update=True)
					if (i in drumPads or i in drumKeys):
						if self.grabbed:
							if (i in drumPads and drumPads[i] == "snare" or
								i in drumKeys and drumKeys[i] == "snare"):
								self.removeSelectedPad()
						else:
							self.addPad(self.editSongT,drumPads[i] if i in drumPads else drumKeys[i], editadd=True)
				newprev.append(i)
		self.prev = newprev

	def updateEdit_BU(self, keys):
		self.updateStats()
		self.addEditPads()
		self.all_notes_list.update()
		self.all_notes_list.draw(self.screen)


		if self.editSongPlaying:
			self.editSongT = self.editSongAccum + pygame.mixer.music.get_pos()

		newprev = []
		for i in allPads:
			# if self.menu.joystick_count != 0:
			if ((self.menu.my_joystick and isinstance(i, int) and self.menu.my_joystick.get_button(i)) or
				self.menu.my_joystick and self.menu.my_joystick.get_hat(0) == i or
				i in keys):
				if i not in self.prev or i in DPAD or i == pygame.K_DOWN or i == pygame.K_UP:
					if (i == 12) or (not self.menu.my_joystick and i == pygame.K_BACKSPACE):
						self.saveRecording()
						self.menu.returnToMenu()
						return
					if (allPads[i] == "start"):
						self.toggleEditPlay()
					if (allPads[i] == "select"):
						self.editSelectPad()
					if not self.editSongPlaying:
						if (allPads[i] == "up"):
							self.editSongAccum += 20
							self.editSongT = self.editSongAccum
							self.addEditPads(update=True)
						if (allPads[i] == "down"):
							self.editSongAccum -= 20
							self.editSongT = self.editSongAccum
							self.addEditPads(update=True)
					if (i in drumPads or i in drumKeys):
						if self.grabbed:
							if (i in drumPads and drumPads[i] == "snare" or
								i in drumKeys and drumKeys[i] == "snare"):
								self.removeSelectedPad()
						else:
							self.addPad(self.editSongT,drumPads[i] if i in drumPads else drumKeys[i], editadd=True)
				newprev.append(i)
		self.prev = newprev

	def update(self,keys):
		if self.free or self.record:
			self.updatePlay(keys)
		if self.edit:
			self.updateEdit(keys)
