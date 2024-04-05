import pygame as pg
from variables import *
import requests


class MenuGroup():
    def __init__(self,menu,groupName, x, y, itemNamesList, replace):
        self.menu = menu
        self.x = x
        self.y = y
        self.groupName = groupName
        self.itemNamesList = itemNamesList
        self.menuItems = []
        self.rotationIndex = 0
        self.replace = replace
        self.addMenuItems()
    
    def addMenuItems(self):
        startingX = self.x
        if not self.replace:
            for itemName in self.itemNamesList:
                newItem = MenuItem(self, self.menu, self.groupName, itemName, startingX, self.y)
                self.menuItems.append(newItem)
                startingX += newItem.width
        else:
            newItem = MenuItem(self, self.menu, self.groupName, self.itemNamesList, startingX, self.y)
            self.menuItems.append(newItem)
        if self.groupName == "Categories":
            self.menu.activeCategory = self.menuItems[0]
            self.menu.mediaTypeCat = self.menu.activeCategory.itemName + " " + self.menu.mediaType
        if self.groupName == "Sort By":
            self.menu.activeSortBy = self.menuItems[0]
            
       
        

class MenuItem():
    def __init__(self, group, menu, groupName, itemName, x, y):
        
        self.menu = menu
        self.group = group
        height = 25
        if groupName == "Media Type": height = 55
        if groupName == "Sort By": height = 40
        self.height = height
        self.lightfont = pygame.font.Font(fp + 'Assets/Fonts/Uni.otf', int(0.7*self.height* (H / 740)))
        self.font = pygame.font.Font(fp + 'Assets/Fonts/Uni Sans Heavy.otf', self.height* int(H / 740))
        self.groupName = groupName
        self.itemName = itemName
        self.sortDir =  itemName != "Name"
        self.rotationIndex = 0

        if type(itemName) is list:
            self.text = itemName[self.rotationIndex]
            
            
       
        elif self.itemName =="Watched": 
            self.text = self.itemName +  " ({})".format(sum([x.watched for x in self.menu.myDB['All ' + self.menu.mediaType]]))
        elif self.itemName =="Watchlist": 
            self.text = self.itemName +  " ({})".format(sum([x.watched for x in self.menu.myDB['All ' + self.menu.mediaType]]))
        else:
            self.text = itemName
        
        
    

        self.subtext = None
        
        self.width = len(self.text)* (self.height * 0.5) + 40
        if groupName == "Sort By": self.width = max(min(len(self.text),6),4)* 25
        # 4-45
        # 6 - 90
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.screen = self.menu.screen

        self.active = False
        self.color = GREY

        if self.group.replace or len(self.group.menuItems) == 0:
            self.active = True
            self.color = WHITE
            self.update()
        self.renderText()
    

    def renderText(self):
        if self.groupName == "Sort By":
            self.txt_surface = self.lightfont.render(self.text, True, self.color)
        else:
            self.txt_surface = self.font.render(self.text, True, self.color)
            if self.subtext:
                self.subtxt_surface = self.lightfont.render(self.subtext, True, self.color)

    def draw(self):
        if self.group.replace and self.active or  (not self.group.replace):
            self.screen.blit(self.txt_surface, (self.rect.x, self.rect.y))
        # if self.subtext:
        #     self.screen.blit(self.subtxt_surface, (self.rect.x, self.rect.y + self.rect.height))
    
    # def updateWatchedCount(self):
    #     for item in self.menu.CategoriesGroup.menuItems:
    #         if item.itemName == "Watched":
    #             item.text = item.itemName +  " ({})".format(sum([x.watched for x in self.menu.myDB['All ' + self.menu.mediaType]]))
    #             item.renderText()
    #             return
        
    def update(self):
        if not self.group.replace:
            for other_tab in self.group.menuItems:
                other_tab.active = other_tab == self
                other_tab.color = WHITE if other_tab == self else GREY
                other_tab.renderText()
            
            if self.groupName == "Categories":
                self.menu.activeCategory = self
                self.menu.mediaTypeCat = self.menu.activeCategory.itemName + " " + self.menu.mediaType
                if self.menu.activeCategory.itemName == "Watched":
                    self.menu.mediaTypeCat = "All " + self.menu.mediaType
                    self.text = self.itemName +  " ({})".format(sum([x.watched for x in self.menu.myDB['All ' + self.menu.mediaType]]))
                elif self.menu.activeCategory.itemName == "Watchlist":
                    self.menu.mediaTypeCat = "All " + self.menu.mediaType
                    self.text = self.itemName +  " ({})".format(sum([x.on_watchlist for x in self.menu.myDB['All ' + self.menu.mediaType]]))
                elif self.itemName != "Watched" and self.itemName!="All":
                    self.menu.activeSortBy = None
            elif self.groupName == "Sort By":
                if self.menu.activeSortBy == self:
                    self.sortDir = not self.sortDir
                self.menu.activeSortBy = self
            self.menu.loadMenuList()
            # self.color = WHITE if self.active else GREY
            
        else:
            self.color = GREEN if self.itemName[self.rotationIndex]== "Watched" else WHITE
            
            self.text = self.itemName[self.rotationIndex]
            # if self.groupName =="Watched": 
            #     self.text += " ({})".format(sum([x.watched for x in self.menu.myDB[self.menu.mediaTypeCat]]))
            # self.updateWatchedCount()
            self.menu.updateTabs()
            self.menu.loadMenuList()

        self.renderText()
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.menu.rememberPosition()
                if type(self.itemName) is list:
                    self.rotationIndex += 1
                    if self.rotationIndex >= len(self.itemName):
                        self.rotationIndex = 0
                    
                    if self.groupName == "Media Type":
                        self.menu.mediaType = self.itemName[self.rotationIndex]
                        self.menu.mediaTypeCat = self.menu.activeCategory.itemName + " " + self.itemName[self.rotationIndex]
                        if "Watch" in self.menu.activeCategory.itemName:
                            self.menu.mediaTypeCat = "All " + self.itemName[self.rotationIndex]
                    
                    
                self.update()
                self.setPosition()
                self.menu.filterList()
        
   

    def setPosition(self):
        key = self.itemName
        if type(self.itemName) is list: key = self.itemName[self.rotationIndex]
        key = key + " " + self.menu.mediaType
        try:
            ind = self.menu.rememberStart[key]
            scr = self.menu.rememberScrollDist[key]
        except:
            ind = 0
            scr = 0
            self.menu.rememberStart[key] = ind
            self.menu.rememberScrollDist[key] = scr
        self.menu.start = ind
        self.menu.scrollDist = scr

    
           
           

