import pygame
from variables import *

class Pad(pygame.sprite.Sprite):
	def __init__(self,song,t,padtype, record,sound=False,missed=False):
		self.sound = pygame.mixer.Sound(fp + "Assets/Sounds/"+padtype+".wav")
		if missed: self.sound.play()
		super().__init__()

		# Variables to hold the height and width of the block
		self.t = t
		self.soundON = sound
		self.missed = missed
		self.song = song

		self.record = record
		self.width = self.song.menu.W // 6
		self.height = self.song.menu.H * (30 / 740)
		self.x = self.song.menu.W * (50/1280)
		self.y = - self.height
		self.vel = self.song.menu.H * (5/740) * song.vel
		self.color = None
		self.alpha = 255

		self.alreadyPlayed = False
		self.padtype = padtype
		if self.padtype == "snare":
			self.x = self.width
			self.XSPEED = self.song.menu.W/256
		if self.padtype == "hihat":
			self.x = 2* self.width
			self.XSPEED = self.song.menu.W/1024
		if self.padtype == "openhihat":
			if self.song.menu.openhihatMode:
				self.x = 2* self.width
				self.XSPEED = self.song.menu.W/1024
			else:
				self.padtype = "tom"
		if self.padtype == "tom":
			self.x = 3*self.width
			self.XSPEED = -1 * self.song.menu.W/1024
		if self.padtype == "crash":
			self.x = 4*self.width
			self.XSPEED = -1 * self.song.menu.W/512
		if self.padtype == "kick":
			self.height *= 0.5
			self.width =  4 * self.width
			self.x = self.song.menu.W // 6
			self.XSPEED = self.song.menu.W/256

		if self.missed or (self.record or not self.song.name):
			self.y = self.song.menu.H - 2 * self.height
			if self.missed:
				self.y = self.song.menu.player.whitebar_rect.y + (self.song.menu.player.whitebar_rect.height - self.height) / 2
			else:
				self.vel *= -1

		self.grabbed = False
		self.justGrabbed = False


		self.image = pygame.Surface([self.width, self.height])
		self.colorPad()
		if self.missed: self.darkenColor()


		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.innerimage = None
		self.innerrect = None
		if self.padtype == "openhihat":
			self.thickness = self.height * 0.15
			self.innerimage = pygame.Surface([self.width - 2 * self.thickness, self.height - 2 * self.thickness])
			self.innerimage.fill(BLACK)


			self.innerrect = self.innerimage.get_rect()
			self.innerrect.x = self.x + self.thickness
			self.innerrect.y = self.y + self.thickness


		self.played = False



	def colorPad(self):
		if not self.color:
			if self.padtype == "snare": self.color = RED
			if self.padtype == "hihat": self.color = YELLOW
			if self.padtype == "openhihat": self.color = YELLOW
			if self.padtype == "tom": self.color = BLUE
			if self.padtype == "crash": self.color = GREEN
			if self.padtype == "kick": self.color = ORANGE
		# print(self.color)
		self.image.fill(self.color)

	def lightenColor(self):

		self.color = tuple([min(255, i + 25) for i in self.color])
		self.alpha = max(0, self.alpha - 25)
		self.image.set_alpha(self.alpha)


	def darkenColor(self):

		self.color = tuple([max(0, i - 150) for i in self.color])
		self.image.set_alpha(200)
		self.colorPad()




	def toggleGrab(self):

		if self.grabbed: self.justGrabbed = True
		self.grabbed = not self.grabbed

		if self.grabbed:

			self.lightenColor()
			self.colorPad()
		elif self.justGrabbed:
			self.color = None
			self.colorPad()
			self.justGrabbed = False

	def drawSelf(self, screen):
		# pygame.draw.rect(screen, self.color, self.rect)
		screen.blit(self.image, (self.rect.x, self.rect.y))
		if self.innerrect:
			screen.blit(self.innerimage, (self.innerrect.x, self.innerrect.y))




	def update(self):
		# self.rect.x = self.x
		if self.song.record or self.song.free:

			self.rect.y += self.vel
			if self.innerimage:
				self.innerrect.y += self.vel

			if not self.record and self.song.name and not self.missed:
				if self.played:

					self.width *= 1.02
					self.height *= 1.02
					self.image = pygame.Surface([self.width, self.height])
					self.rect.x -= self.XSPEED
					if self.innerimage:
						self.innerimage = pygame.Surface([self.innerimage.get_width()*1.02, self.innerimage.get_height()*1.02])
						self.innerrect.x -= self.XSPEED
					self.colorPad()
					self.lightenColor()
					if not self.alreadyPlayed:
						self.song.hits += 1
						self.song.streak += 1
						if not self.missed: self.song.totalNotes += 1
					self.alreadyPlayed = True


				if self.rect.y >= self.song.menu.player.bar_rect.y +self.song.menu.player.barheight and not self.alreadyPlayed:
					if not self.alreadyPlayed:
						self.song.missed += 1
						self.song.longestStreak = max(self.song.longestStreak, self.song.streak)
						self.song.streak = 0
						if not self.missed: self.song.totalNotes += 1
					# self.image.fill(BLACK)
					self.alreadyPlayed = True

			elif not self.missed:
				if self.rect.y >= self.song.menu.H*7/8 - self.vel and not self.played:
					if self.soundON: pygame.mixer.Sound.play(self.sound)
					self.played = True

			if (self.song.free and not self.record) and self.rect.y + self.height > self.song.menu.H:
				self.kill()

			if (self.record or not self.song.name) and self.rect.y  < 0:
				self.kill()

		if self.song.edit:
			self.rect.y = self.song.menu.player.whitebar_rect.y - (self.t - self.song.editSongT)
			if self.innerimage:
				self.innerrect.y = self.song.menu.player.whitebar_rect.y - (self.t - self.song.editSongT) + self.thickness

			if self.rect.y + self.height > self.song.menu.H:
				self.kill()
			if self.rect.y  < 0:
				self.kill()
