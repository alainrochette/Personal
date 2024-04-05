from variables import *
from Database import *
from TVShow import *
from InputBox import *
from MenuTab import *
import pygame
import math
import shutil
import os
from PIL import Image, ImageFilter
import requests 
import copy

PopularURL = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + api_key
}

class Menu:

	def __init__(self,screen, clock, dim):

		self.menuType = "Database"
		self.myDB = None
		self.DB = Database(self)
		self.myDB = self.DB.myDB
		
		
		# self.onlyWatched = False

		self.mediaType = "TV Shows"
		self.mediaTypeCat = "All TV Shows"
		
		self.W = dim[0]
		self.H = dim[1]
		
		self.theme = BLACK
		self.theme_opp = WHITE
		self.theme_grey = GREY
		
		self.clock = clock
		self.done = False

		self.showingDetails = False
		self.VScrollSpeed = 0
		self.HScrollSpeed = 0
		self.scrollEdge = 0.25

		self.ListN = 15
		self.start = 0
		self.screen = screen

		

		self.menuTabs = []
		self.menuList = []
		self.menuTabHeight = self.H/7
		self.maxMenuTabHeight = 2 * self.menuTabHeight

		self.onTopMenu  = False
		self.startHoverMenuAnimT = 0
		self.startSelectAnimT = 0
		self.SelectAnimDur = 200
		self.startLagT = 0

		self.scrollDist = 0
		self.scrollVel = 0
		self.spacing = 20
		
		self.sortBy = "Date"
		self.activeCategory = None
		self.activeSortBy = None
		self.menuGroups = []
		self.inputBox = InputBox(self,0,self.spacing*2,self.W/5,self.H/self.ListN)
		self.CategoriesGroup = MenuGroup(self,"Categories",14 * self.spacing,self.spacing,
				   						["All","Watched","Watchlist","Popular", "Top Rated","Upcoming",],replace=False)
		self.SortByGroup = MenuGroup(self,"Sort By",14 * self.spacing, 3 *self.spacing,
				   						["Name","Air Date","Popularity", "Rating", "My Ranking"],replace=False)
		
		self.MediaGroup = MenuGroup(self,"Media Type",0,0,["TV Shows", "Movies"],replace=True)
		# self.WatchedGroup = MenuGroup(self,"Watched", self.spacing, 3*self.spacing,["Watched", "Not Watched"],replace=True)
		
		self.menuGroups = [self.MediaGroup,self.CategoriesGroup, self.SortByGroup]

		self.rememberStart = {}
		self.rememberScrollDist = {}

		for mediaType in self.myDB:
			self.rememberStart[mediaType] = 0
			self.rememberScrollDist[mediaType] = 0
	
		# self.updateTabs()


		self.imageUrl = "X"

		
		self.selectedOption = 0
		self.selectedMedia = None

		self.prevSelectionOption = 0
		
		self.menuList = []
		

		self.newPressedKeys = []
		self.prevPressedKeys = []
		self.pressedKeys = []

		self.font = pygame.font.Font(fp + 'Assets/Fonts/UNI.otf', 30 * int(self.H / 740))
		self.bigfont = pygame.font.Font(fp + 'Assets/Fonts/Uni Sans Heavy.otf', 30* int(self.H / 740))
		self.biggestfont = pygame.font.Font(fp + 'Assets/Fonts/Uni Sans Heavy.otf', 50* int(self.H / 740))
		
		
		
		self.loadMenuList()
		self.filterList()
		self.loadMenu()
		
	
	def rememberPosition(self):
		self.rememberStart[self.activeCategory.itemName + " " + self.mediaType] = self.start
		self.rememberScrollDist[self.activeCategory.itemName + " " + self.mediaType] = self.scrollDist

		
        
	
				


		self.DB.saveMyDB()

	def getNewShows(self):
		lets = "abcdefghijklmnopqrstuvwxyz"
		lastone = "aaa"
		for i in lets:
			for j in lets:
				for k in lets:
					txt = "{}{}{}".format(i,j,k)
					if txt >= lastone:
						self.inputBox.text = txt
						print("{}{}{}".format(i,j,k))
						self.inputBox.searchDB()
				print(len(self.myDB["Shows"]),"SHOWS")
		self.DB.saveMyDB()

	def addText(self, text, color, center, big=False, bgcolor=None, align="center",sub=None):

		for i in range(len(text)):
			if ord(text[i]) > 0xFFFF:
				l = list(text)
				l[i] = "?"
				text = "".join(l)

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

	def loadMenuList(self, nextPage=False):
		
		if self.activeCategory.itemName == "Popular" or self.activeCategory.itemName == "Upcoming" or self.activeCategory.itemName == "Top Rated":
			
			self.activeCategoryPage = 1 if not nextPage else self.activeCategoryPage + 3
			# self.sortBy = self.activeSortBy.itemName

			# for page in range(self.activeCategoryPage + 4):
			url = "https://api.themoviedb.org/3/{}/{}?language=en-US&page={}".format("movie" if self.mediaType == "Movies" else "tv",self.activeCategory.itemName.lower().replace(" ","_"),self.activeCategoryPage)
			response = requests.get(url, headers=headers)
			AllMedia  = response.json().get('results', [])
			if not nextPage: 
				self.myDB[self.mediaTypeCat] = []
			for media in AllMedia:
				tvdb_id  = media.get('id')
				if not (self.mediaType == "TV Shows" and self.activeCategory.itemName == "Upcoming"):
					if self.mediaType == "TV Shows":
						newMedia = self.DB.addTVShow(tvdb_id,media)
					elif self.mediaType == "Movies":
						newMedia = self.DB.addMovie(tvdb_id,media)
					if newMedia not in self.myDB[self.mediaTypeCat]: 
						self.myDB[self.mediaTypeCat].append(newMedia)
							# print(movie.name)
		
			# self.sortBy = self.activeCategory.itemName
			# self.refreshImages()

	def getActorIDs(self, searchText):
		actorIDs = []
		for actorID in self.myDB["All People"]:
			if searchText.lower() in self.myDB["All People"][actorID].lower():
				actorIDs.append(actorID)
		return actorIDs


	
	def filterList(self, all=False):
		searchText = self.inputBox.text if self.inputBox.text != self.inputBox.defaultText  else ""
		actorIDs = []
		if len(searchText) > 5 and " " in searchText:
			actorIDs = self.getActorIDs(searchText)
		
		filteredList = list(filter(lambda x: x.visible and ((x.watched and self.activeCategory.itemName == "Watched") or (x.on_watchlist and self.activeCategory.itemName == "Watchlist") or ("Watch" not in self.activeCategory.itemName  and x.id != "X")), 
			     			filter(lambda x: searchText in x.name.lower() or (set(actorIDs) & set(x.castIDs)), self.myDB[self.mediaTypeCat])))

		
		# prevMenuList = self.menuList

		if self.activeSortBy:
			if self.activeSortBy.itemName == "Air Date":
				filteredList = list(sorted(filteredList, key=lambda x: x.date, reverse=self.activeSortBy.sortDir))

			elif self.activeSortBy.itemName == "Name":
				filteredList = list(sorted(filteredList, key=lambda x: x.name, reverse=self.activeSortBy.sortDir))
			elif self.activeSortBy.itemName == "My Ranking":
				filteredList = list(filter(lambda x: x.myRating != None, filteredList))
				filteredList = list(sorted(filteredList, key=lambda x: x.name, reverse=False))
				filteredList = list(sorted(filteredList, key=lambda x: x.myRating, reverse=self.activeSortBy.sortDir))
			elif self.activeSortBy.itemName == "Rating":
				# filteredList = list(filter(lambda x: x.myRating != None, filteredList))
				filteredList = list(sorted(filteredList, key=lambda x: x.rating, reverse=self.activeSortBy.sortDir))
				# filteredList = list(sorted(filteredList, key=lambda x: x.myRating, reverse=True))

		
		self.menuList = list(filteredList)
		self.refreshImages()
		# for media in self.menuList:
		# 	media.loadImg()
		
	def refreshImages(self,prevMenuList=[]):
		for prevMedia in prevMenuList:
			if prevMedia not in self.menuList[self.start: self.start + self.ListN]:
				# pass
				prevMedia.unloadImg()
		for media in self.menuList[self.start: self.start + self.ListN]:
			# pass
			# if media not in prevMenuList or media.posterImg == None:
			if media.posterImg == None:
				media.loadImg()

	def loadMenu(self):
		if self.menuType == "Database":
			i = 0
			options_i = self.start
			
			nowT = pygame.time.get_ticks()
			animPerc = 1
			if abs(self.scrollVel) < 4 and nowT - self.startSelectAnimT <= self.SelectAnimDur:
				animPerc = min(1,(nowT - self.startSelectAnimT) / self.SelectAnimDur)
			
			for media in self.menuList[self.start: self.start + self.ListN]:
				try:
					shouldBeX =  (media.posterImg.get_size()[0] + self.spacing) * i  - self.scrollDist
				except:
					media.loadImg()
					shouldBeX =  (media.posterImg.get_size()[0] + self.spacing) * i  - self.scrollDist

				
				
				if media.xPos == None: media.xPos = shouldBeX
				if media.yPos == None: media.yPos = self.menuTabHeight + self.spacing 

				
				if media == self.selectedMedia:
					# show.yPos -= heightPerc*self.spacing /2
					media.xPos = (shouldBeX) +  animPerc * 0.5 * self.spacing* (self.mouseX - (media.xPos + media.posterImg.get_size()[0]/2))/(media.posterImg.get_size()[0]/2)
					media.yPos = (self.menuTabHeight + self.spacing ) +  animPerc * 0.5 * self.spacing* (self.mouseY - (media.yPos + media.posterImg.get_size()[1]/2))/(media.posterImg.get_size()[1]/2)
					
					yy =  self.menuTabHeight + self.spacing  + media.posterImg.get_size()[1] + self.spacing

					title = media.name 
					subtitle =  str(media.date[0:4]) 
					clr = WHITE
					# if media.watched and self.activeCategory.itemName != "Watched": clr = GREEN
					# if media.on_watchlist and self.activeCategory.itemName != "Watchlist": clr = BLUE
					# if not media.watched and media.on_watchlist: clr = BLUE
					self.addText(title, clr,(shouldBeX, yy), big=True,bgcolor=self.theme,align="left", sub=subtitle)
					# print(media.myRating)
					try:
						if media.watched: self.addText(str(media.myRating), clr,(shouldBeX + 250, yy + 35), big=True,bgcolor=self.theme,align="left")
					except: pass
					

				else:
					
					media.xPos +=  animPerc * ((shouldBeX ) - media.xPos)
					media.yPos +=  animPerc * (( self.menuTabHeight + self.spacing ) - media.yPos)
				
				media.draw(self)

				# if media == self.selectedMedia:
				# try:
				# 	for icon in media.icons:
				# 		icon.update()
				# except:
				# 	pass
				# if media.icons == [] and media.highlighted:
				# 	media.loadIcons()
				# try:
				# 	for icon in media.icons:
				# 		icon.update()
				# except:
				# 	pass
				# else:
				# 	media.icons = []
				i += 1
				options_i += 1

	def saveImg(self, media):
		if media.imageUrl== None:
			pass
		else:
			if not os.path.isfile("Assets/Posters/{}/{}.jpg".format(self.mediaType,media.id)):
				newUrl = media.imageUrl.replace("w1280","w342")
				data = requests.get(newUrl).content
					
				f = open("Assets/Posters/{}/{}.jpg".format(self.mediaType,media.id),'wb')
				f.write(data)
				f.close()


	def updateTabs(self):
		for item in self.CategoriesGroup.menuItems:
			if item.itemName == "Watched":
				item.text = item.itemName +  " ({})".format(sum([x.watched for x in self.myDB['All ' + self.mediaType]]))
				item.renderText()
			if item.itemName == "Watchlist":
				item.text = item.itemName +  " ({})".format(sum([x.on_watchlist for x in self.myDB['All ' + self.mediaType]]))
				item.renderText()

		for group in self.menuGroups:
			for tab in group.menuItems:
				# tab.update()
				tab.draw()


	def updatePressed(self):
		if self.HScrollSpeed == 0:
			
			self.mouseX =  pygame.mouse.get_pos()[0]
			self.mouseY =  pygame.mouse.get_pos()[1]
			mediaSelected = False
			for media in self.menuList[self.start: self.start + self.ListN]:
				if media.isHighlighted(self.mouseX,self.mouseY):
					media.highlighted = True
					if self.selectedMedia != media:
						self.startSelectAnimT = pygame.time.get_ticks()
					self.selectedMedia = media
					mediaSelected = True
				else:
					media.highlighted = False
			if not mediaSelected:
				if self.selectedMedia: self.startSelectAnimT = pygame.time.get_ticks()
				self.selectedMedia = None
			for event in pygame.event.get():
				
				self.inputBox.handle_event(event)
				if event.type in [pygame.MOUSEWHEEL]:
					self.VScrollSpeed = event.y
					self.HScrollSpeed = event.x*1.5
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					for group in self.menuGroups:
						for tab in group.menuItems:
							tab.handle_event(event)
					for media in self.menuList[self.start: self.start + self.ListN]:
						new = media.handle_event(event)
						if new == "icons": 
							
							self.updateTabs()
							self.filterList()
						if new == "details":
							self.start = self.menuList.index(media)
							self.scrollDist = -100

		
				if event.type == pygame.QUIT:
					self.done = True
					
		
		if not self.done:
			nowT =  pygame.time.get_ticks()
			self.prevPressedKeys = self.pressedKeys


			self.pressedKeys = []
			self.newPressedKeys = []
			keys = pygame.key.get_pressed()
			for k in compKeys:
				if keys[k]: 
					self.pressedKeys.append(compKeys[k])
					if compKeys[k] not in self.prevPressedKeys: 
						self.newPressedKeys.append(compKeys[k])
						
			
			


			self.newPressedKeys = list(set(self.newPressedKeys))



			if self.HScrollSpeed > 0:
				self.HScrollSpeed = math.floor(0.98*(min(self.HScrollSpeed,10)))
			elif self.HScrollSpeed < 0:
				self.HScrollSpeed = math.ceil(0.98*(max(self.HScrollSpeed,-10)))
			else:
				self.HScrollSpeed = 0

			if self.mouseY <= self.menuTabHeight / 2 and  nowT > 2000:
				self.onTopMenu  = True
				if self.startHoverMenuAnimT == 0: self.startHoverMenuAnimT = nowT
			elif self.mouseY > self.menuTabHeight:
				if self.onTopMenu: 
					self.startHoverMenuAnimT = nowT
				if nowT - self.startHoverMenuAnimT > self.SelectAnimDur:
					self.startHoverMenuAnimT = 0
				self.onTopMenu = False

			if inKeys(["right"], self.newPressedKeys):
				if self.scrollVel == 0: self.start += 1
				# self.filterList()
				self.refreshImages()
				self.startLagT = nowT
			elif inKeys(["right"], self.pressedKeys):
				if nowT - self.startLagT > self.SelectAnimDur:
					self.scrollVel += 0.5
			elif inKeys(["left"], self.newPressedKeys):
				if self.scrollVel == 0: self.start = max(self.start - 1, 0)
				# self.filterList()
				
				self.refreshImages()
				self.startLagT = nowT
			elif inKeys(["left"], self.pressedKeys):
				if nowT - self.startLagT > self.SelectAnimDur:
					self.scrollVel -= 0.5
			elif inKeys(["up"], self.newPressedKeys):
				if self.selectedMedia:
					self.selectedMedia.upRating()
					# self.updateTabs()
					# self.filterList()
			elif inKeys(["down"], self.newPressedKeys):
				if self.selectedMedia:
					# self.selectedMedia.toggleWatchList()
					self.selectedMedia.downRating()
					# self.updateTabs()
					# self.filterList()
			
			
			elif not self.showingDetails:
				if self.mouseX >= (1-self.scrollEdge)*self.W and self.mouseY > self.menuTabHeight + self.spacing :
					self.scrollVel = 1.5 ** (10 * (self.mouseX - (1-self.scrollEdge)*self.W) / (self.scrollEdge*self.W))
				elif self.mouseX <= self.scrollEdge*self.W and self.mouseY > self.menuTabHeight + self.spacing :
					self.scrollVel = -1.5 ** (10 * (self.scrollEdge*self.W - self.mouseX ) / (self.scrollEdge*self.W))
				elif abs(self.HScrollSpeed) > 0:
					self.scrollVel += self.HScrollSpeed 
				else:
					self.startLagT = nowT
					self.scrollVel *= 0.9
					if abs(self.scrollVel) < 0.002: self.scrollVel = 0
			elif self.showingDetails:
				self.scrollVel = 0
			self.scroll()
		
		

	def scroll(self):
		if self.scrollVel != 0:
			try:
				wid = self.menuList[self.start: self.start + self.ListN][0].posterImg.get_size()[0] + self.spacing
				
				if self.scrollVel < 0 or (self.scrollVel > 0 and self.start <= len(self.menuList) - self.ListN / 4):
					self.scrollDist += self.scrollVel
					dir = 1 if self.scrollDist > 0 else -1
					shift = False
					self.scrollDist = max(-1*wid, self.scrollDist)
					if self.scrollDist >= 2*wid:
						self.start += 1
						shift = True
						

					if self.scrollDist < 0 and self.start > 0:
						self.start -= 1
						shift = True
					if shift:
						self.start = max(0,self.start)
						
						# if self.start != 0: 
						self.scrollDist -= wid*dir
						self.scrollDist = max(-1*wid, self.scrollDist)
					
						self.refreshImages()
						# self.filterList()
				elif self.scrollVel > 0 :
					if self.activeCategory != "All":
						self.loadMenuList(nextPage=True)
			except:
				pass
		# for show in self.menuList:


		

		# mid = self.ListN // 2

		# if xvel == 1:
		# self.scrollDist *= 1.1
		# self.scrollDist = min(50,self.scrollDist)
		# self.start += int(xvel)
		
		
		# if self.selectedOption == self.ListN // 2:
		# 	if x_len < self.ListN:
		# 		self.selectedOption -= xvel
		# 	else:
		# 		if self.start - xvel < 0 or self.start - xvel > x_len -1:
		# 			self.selectedOption -= xvel
		# 		else:
		# 			self.start -= xvel
		# else:
		# 	if self.selectedOption - xvel > self.ListN - 1 or self.selectedOption - xvel < 0:
		# 		self.start -= xvel
		# 	else:
		# 		self.selectedOption -= xvel
		# if abs(xvel) == 1:
		# 	self.startAnimationT = pygame.time.get_ticks()
		# self.selectedOption = min(x_len - 1,min(max(0,self.selectedOption),(x_len-self.start - 1)),self.selectedOption)
		# self.start = min(max(0,self.start),x_len - self.ListN//2)
		# self.filterList()


	def update(self):
		
		self.screen.fill(self.theme)

		self.updatePressed()

		self.loadMenu()
		self.inputBox.draw()
		for group in self.menuGroups:
			for tab in group.menuItems:
				# tab.update()
				tab.draw()
