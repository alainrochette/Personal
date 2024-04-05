import pygame as pg
from variables import *
import requests

api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'

class InputBox:

    def __init__(self, menu, x, y, w, h, text=''):
        self.menu = menu
        self.defaultText = "Search..."
        self.rect = pg.Rect(x, y, w, h)
        self.screen = self.menu.screen
        self.color = GREY
        self.text = self.defaultText
        self.font = pg.font.Font(fp + 'Assets/Fonts/UNI.otf', 40 * int(H / 740))
        self.txt_surface =  self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     # If the user clicked on the input_box rect.
        #     if self.rect.collidepoint(event.pos):
        #         # Toggle the active variable.
        #         self.active = not self.active
        #     else:
        #         self.active = False
        #     # Change the current color of the input box.
        #     self.color = WHITE if self.active else GREY
        if event.type == pg.KEYDOWN:
            # if self.active:
            
            if event.key == pg.K_RETURN:
                self.searchDB()
                self.menu.updateTabs()
                # self.text =  self.defaultText 
                self.color = GREY
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
                self.menu.filterList()
            else:
                
                if self.text == self.defaultText:
                    
                    self.text = event.unicode
                    self.menu.filterList()
                else:
                    self.text += event.unicode
                    self.menu.filterList()
            # Re-render the text.
            self.renderText()
            
    def renderText(self):
        txt = self.text
        clr = WHITE
        if txt == '' or txt == self.defaultText: 
            txt = self.defaultText
            clr = GREY
        self.txt_surface = self.font.render(txt, True, clr)

    def searchDB(self):
        url = "https://api.themoviedb.org/3/search/{}?query={}&include_adult=true&language=en-US&page=1".format("tv" if self.menu.mediaType == "TV Shows" else "movie", self.text)
        
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_key
        }

        response = requests.get(url, headers=headers)
        medias = response.json().get('results', [])
        foundMedia = False
        for show in medias:
            foundMedia = True
            tvdb_id  = show.get('id')
            if self.menu.mediaType == "TV Shows":
                self.menu.DB.addTVShow(tvdb_id,show)
            if self.menu.mediaType == "Movies":
                self.menu.DB.addMovie(tvdb_id,show)
        if not foundMedia and " " in self.text:
            ids = self.menu.DB.addPerson(self.text)
            for personId in ids:

                url = "https://api.themoviedb.org/3/person/{}/{}_credits?language=en-US".format(personId, "movie" if self.menu.mediaType == "Movies" else "tv")

                response = requests.get(url, headers=headers)

                deets = response.json()
                if 'cast' in deets:
                    for media in deets['cast']:
                        tvdb_id  = media.get('id')
                        if self.menu.mediaType == "TV Shows":
                            self.menu.DB.addTVShow(tvdb_id,media,int(personId))
                        if self.menu.mediaType == "Movies":
                            self.menu.DB.addMovie(tvdb_id,media,int(personId))
        self.menu.filterList()

            # if "US" in orig_country:
            #     total_show_i += 1
            #     self.menuallShows[tvdb_id] = show
                
            # show_i += 1
        # print(response.text)
    # def update(self):
    #     # Resize the box if the text is too long.
    #     width = max(200, self.txt_surface.get_width()+10)
    #     self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        # pg.draw.rect(self.screen, self.color, self.rect, 2)
