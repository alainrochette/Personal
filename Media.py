import requests
from variables import * 
from datetime import datetime
import os
import threading
from MediaIcons import *

image_prefix = 'http://thetvdb.com/banners/'
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'

class Media():
    def __init__(self,rawMedia,id,tvOrMovie):
        self.rawMedia = rawMedia
        self.isTVShow = tvOrMovie == "TV Show"
        self.isMovie = tvOrMovie == "Movie"
        self.id = id
        try:
            self.name = rawMedia['name'] 
        except:
            self.name = rawMedia["title"]
        try:
            self.date = rawMedia['first_air_date'] 
        except:
            self.date = rawMedia['release_date']
        self.overview = rawMedia['overview']
        self.genreIDs = rawMedia['genre_ids']
        self.castIDs = []

        self.imageUrl = None
        self.posterFolder = "Assets/Posters/TV Shows/" if self.isTVShow else "Assets/Posters/Movies/"
        self.get_show_image()
        # self.get_cast()

        self.rating = rawMedia['vote_average']
        self.myRating = None
        self.watched = False
        self.liked = False
        self.on_watchlist = False
        self.date_added = datetime.now()
        self.visible = True
        self.xPos =  None
        self.yPos = None
        self.imgHidden = True
        self.icons = []
        self.highlighted = False
        
        # print(self.name, self.date_added)
    
    def loadIcons(self):
        self.icons = []
        try:
            icons = self.icons
        except:
            self.icons = []
        if self.icons == []:
            # for i in range(10):
            #     newIcon = MediaIcon(self,"star")
            #     self.icons.append(newIcon)
            if self.watched:
                newIcon = MediaIcon(self,"checked")
            else:
                newIcon = MediaIcon(self,"unchecked")
                self.icons.append(newIcon)
                if self.on_watchlist:
                    newIcon = MediaIcon(self,"added")
                else:
                    newIcon = MediaIcon(self,"add")
            self.icons.append(newIcon)
            
    
    def unloadIcons(self):
        try:
            icons = self.icons
        except:
            self.icons = []
        if self.icons != []:
            self.icons = []
            

    def setPosterFolder(self, isTV):
        self.isTVShow = isTV
        self.posterFolder = "Assets/Posters/TV Shows/" if self.isTVShow else "Assets/Posters/Movies/"
        
    def setWatched(self):
        self.watched = True
        self.on_watchlist = False
    
    def setUnwatched(self):
        self.watched = False
    
    def setWatchlist(self):
        if not self.watched:
            self.on_watchlist = True
    
    def setUnwatchlist(self):
         if not self.watched:
            self.on_watchlist = False

        
    def printAttributes(self):
        attrs = vars(self)
        # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
        # now dump this in some way or another
        print(', '.join("%s: %s" % item for item in attrs.items()))

    



    def get_show_image(self):
        image_prefix = 'https://image.tmdb.org/t/p/w342/'
        if self.isTVShow:
            url = "https://api.themoviedb.org/3/tv/{}/images".format(self.id)

            headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer " + api_key
                }

            

            response = requests.get(url, headers=headers)

            images = response.json()

            poster_url = ""
            if "posters" in images:
                for poster in images['posters']:
                    if poster['iso_639_1'] == 'en' or poster['iso_639_1'] == None:
                        poster_url = poster['file_path']
                        break
            if poster_url == "": 
                try:
                    poster_url = images['posters'][0]['file_path']
                except:
                    poster_url = ""
            
            if poster_url == "":
                self.imageUrl = None
            else:
                poster_image_url = image_prefix + poster_url
                self.imageUrl = poster_image_url
        else:
            try:
                self.imageUrl = image_prefix +  self.rawMedia['poster_path']
            except:
                self.imageUrl = None 
    
    # def unloadImgThread(self):
    #     x = threading.Thread(target=self.unloadImg())
    #     x.start()

    def unloadImg(self):
        self.posterImg = None
        self.unloadIcons()
        # try:
        #     for icon in self.icons:
        #         icon.iconImg = None
        # except:
        #     pass
        # try:
        #     os.remove(self.posterFolder + "{}.jpg".format(self.id))
        # except:
        #     pass
    
    # def loadImgThread(self):
        
    #     x = threading.Thread(target=self.loadImg())
    #     x.start()

    def loadImg(self):
        # print("loading Img..")
        assetLocation = self.posterFolder + "{}.jpg".format(self.id)

        
        try:
            self.posterImg = pygame.image.load(assetLocation)
            # self.imageUrl = self.imageUrl
        except:
            if self.imageUrl== None:
                self.posterImg = pygame.image.load(self.posterFolder + "/blank.jpg")
                # self.imageUrl = None
            else:
                newUrl =self.imageUrl.replace("w1280","w342")
                data = requests.get(newUrl).content
                    
                f = open(assetLocation,'wb')
                f.write(data)
                f.close()

                self.posterImg = pygame.image.load(assetLocation)
                self.imageUrl = newUrl

        size = self.posterImg.get_size()
        rect_image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(rect_image, (255, 255, 255), (0, 0, *size), border_radius=30)


        self.posterImg = self.posterImg.copy().convert_alpha()
        
        self.posterImg.blit(rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN) 
        
        
        # self.posterImg.blit(watched, (0, 0), None, pygame.BLEND_RGBA_MIN) 

        if self.imageUrl== None:
            txt = pygame.font.Font(fp + 'Assets/Fonts/UNI.otf', 40 * int(H / 740)).render(self.name, True, WHITE, BLACK)
            self.posterImg.blit(txt,(0,0))
        self.imageHidden = False
        self.xPos =  None
        self.yPos = None
    
         
    def isHighlighted(self, mouseX, mouseY):
        try:
            rect_image  = self.posterImg.get_rect(topleft=(self.xPos, self.yPos))
            # if mouseX >= self.xPos and mouseX <= self.xPos + self.posterImg.get_size()[0]:
            #     return True
            if rect_image.collidepoint((mouseX,mouseY)):
                return True
        except:
            
            pass
        return False
    
    def upRating(self):
        if self.watched:
            try: rating = int(self.myRating)
            except: rating = 0
            self.myRating = min(5,rating + 1)
        
    def downRating(self):
        if self.watched:
            try: rating =int(self.myRating)
            except: rating = 0
            self.myRating = max(-2,rating - 1)

    def toggleWatched(self):
        self.watched = not self.watched
        if self.watched: self.on_watchlist = False
    
    def toggleWatchList(self):
        if not self.watched:
            self.on_watchlist = not self.on_watchlist
    
    

    def handle_event(self, event):
        # if event=="toggleWatched" or 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        
            # # If the user clicked on the input_box rect.
            # size = self.posterImg.get_size()
            # rect_image = pygame.Surface(size, pygame.SRCALPHA)
            # pygame.draw.rect(rect_image, (255, 255, 255), (0, 0, *size), border_radius=30)
            for icon in self.icons:
                # if icon.type == "unchecked": print(event.pos, event.pos[0]<= icon.x + icon.iconImg.get_size()[0])
                rect_image  = icon.iconImg.get_rect(topleft=(icon.x, icon.y))
                if rect_image.collidepoint(event.pos):
                # if event.pos[0]<= icon.x + icon.iconImg.get_size()[0] and event.pos[0]>= icon.x and event.pos[1]<= icon.y + icon.iconImg.get_size()[1] and event.pos[1]>= icon.y:
                  
                    if icon.type == "checked":
                        self.setUnwatched()
                    elif icon.type == "unchecked":
                        self.setWatched()
                    elif icon.type == "add":
                        self.setWatchlist()
                    elif icon.type == "added":
                        self.setUnwatchlist()
                    return "icons"
            try:
                rect_image  = self.posterImg.get_rect(topleft=(self.xPos, self.yPos))
                if rect_image.collidepoint(event.pos):
                    # self.toggleDetails()
                    print("See more details")
                    return "details"
                    # if self.watched:
                    #     self.setUnwatched()
                    # else:
                    #     self.setWatched()

                    # return True
            except:
                pass
            
            # return True
           
        return False
                # Toggle the active variable.
                # self.menu.activateTab(self)
            # else:
            #     self.active = False
    
    def draw(self, menu):
        menu.screen.blit(self.posterImg,(self.xPos,self.yPos))
        if menu.selectedMedia == self:
            self.loadIcons()
            for icon in self.icons:
                # if icon.type=="star" and self.watched:
                #     icon.x = self.xPos + icon.spacing * icon.rating_i
                #     icon.y = self.yPos +  0.9 * self.posterImg.get_size()[1]
                #     menu.screen.blit(icon.iconImg,(icon.x,icon.y))
                if icon.type=="checked" or icon.type=="unchecked":
                    icon.x = self.xPos + self.posterImg.get_size()[0] - icon.iconImg.get_size()[0]*1.5
                    icon.y = self.yPos + icon.iconImg.get_size()[1]*0.5
                
                    menu.screen.blit(icon.iconImg,(icon.x,icon.y))
                if icon.type=="add" or icon.type=="added":
                    icon.x = self.xPos + self.posterImg.get_size()[0] - icon.iconImg.get_size()[0]*3.2
                    icon.y = self.yPos + icon.iconImg.get_size()[1]*0.5
                
                    menu.screen.blit(icon.iconImg,(icon.x,icon.y))
                
                # self.highlighted = True
            # else:
            #     self.highlighted = False
            #     self.iconImg = None
        