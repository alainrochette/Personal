import pygame


class MediaIcon():
    def __init__(self, media, type):
        self.media = media
        self.rating_i = len(self.media.icons)
        self.spacing = 0.05 * self.media.posterImg.get_size()[1]
        self.iconFolder = "Assets/Icons/"
        self.type = type
        self.highlighted = False
        self.iconImg = None
        self.x = self.y = 0
        self.loadImg()

        # self.x = self.media.xPos + self.spacing * self.rating_i
        # self.y = self.media.yPos +  0.9 * self.media.posterImg.get_size()[1]
    
    def update(self):
        pass
        # if self.media.highlighted:
        #     self.x = self.media.xPos + self.spacing * self.rating_i
        #     self.y = self.media.yPos +  0.9 * self.media.posterImg.get_size()[1]
        #     if not self.highlighted or not self.iconImg:
        #         self.loadImg()
        #         self.media.posterImg.blit(self.iconImg,(self.x - self.media.xPos,self.y- self.media.yPos))
            
        #     self.highlighted = True
        # else:
        #     self.highlighted = False
        #     self.iconImg = None
    
    def loadImg(self):
        assetLocation = self.iconFolder + "{}.png".format(self.type)
        self.iconImg = pygame.image.load(assetLocation)
        
        
        # self.media.posterImg.blit()
        # size = self.iconImg.get_size()
        # rect_image = pygame.Surface(size, pygame.SRCALPHA)
        # pygame.draw.rect(rect_image, (255, 255, 255), (0, 0, *size), border_radius=30)


        # self.posterImg = self.posterImg.copy().convert_alpha()
        
        # self.posterImg.blit(rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN) 
        
        
        # # self.posterImg.blit(watched, (0, 0), None, pygame.BLEND_RGBA_MIN) 

        # if self.imageUrl== None:
        #     txt = pygame.font.Font(fp + 'Assets/Fonts/UNI.otf', 40 * int(H / 740)).render(self.name, True, WHITE, BLACK)
        #     self.posterImg.blit(txt,(0,0))
        # self.imageHidden = False
        # self.xPos =  None
        # self.yPos = None