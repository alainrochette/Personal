import requests
from PIL import Image
import json
import numpy as np

import cv2


search  = "https://api.themoviedb.org/3/search/tv?query=fboy&include_adult=true&language=en-US&page=1"


# 3 = right
# 2 = left
# 0 = up
# 1 = down
# 127 = backspace
# 48-57 = 0-9
S_WIDTH = 1280
S_HEIGHT = 1919
LEFT_ARROW = 2
RIGHT_ARROW = 3
UP_ARROW = 0
DOWN_ARROW = 1
BACKSPACE = 127
A_KEY = 97
S_KEY = 115
W_KEY = 119
D_KEY = 100
WOULD_WATCH = W_KEY = 119
HAVENT_SEEN = S_KEY = 115
LIKED = D_KEY = 100
DIDNT_LIKE = A_KEY = 97
EXIT = 27

SELECT_TIMER = 1

BUTTON_RADIUS = 80
BUTTON_COLOR = (255,255,255)
TEXT_COLOR = (0,0,0)
BUTTON_THICKNESS = 1

WOULD_WATCH_CENTER = (S_WIDTH//2,int(S_HEIGHT*9/10)-2*BUTTON_RADIUS)
HAVENT_SEEN_CENTER = (S_WIDTH//2,int(S_HEIGHT*9/10))
LIKED_CENTER = (int(S_WIDTH*(3/4)),int(S_HEIGHT*9/10))
DIDNT_LIKE_CENTER = (int(S_WIDTH*1/4),int(S_HEIGHT*9/10))


HAVENT_SEEN_COLOR = (0,0,0)
WOULD_WATCH_COLOR = (50,80,50)
LIKED_COLOR = (150,255,150)
DIDNT_LIKE_COLOR = (150,150,255)
SELECTED_THICKNESS = 20


url = "https://api.themoviedb.org/3/authentication"
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'
image_prefix = 'http://thetvdb.com/banners/'

class TVWindow():
        
    def __init__(self):
        self.image = None

    

    def get_show_image(self, tvdb_id,i):

        url = "https://api.themoviedb.org/3/tv/{}/images".format(tvdb_id)

        headers = {
                "accept": "application/json",
                "Authorization": "Bearer " + api_key
            }

        # # TVDB
        # TVDB_API_KEY = '[your api key]'
        # TVDB_USERNAME = '[your username]'
        # TVDB_USERKEY = '[your user key]'
        image_prefix = 'https://image.tmdb.org/t/p/w1280/'

        # get token
        response = requests.get(url, headers=headers)


        with open('data_image{}.json'.format(i), 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
    

        images = response.json()

        # this returns full size images by default (use the thumbnail image if possible)
        # it is recommend to check the language and image size to work best in your app
        poster_url = ""
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
            saved_img = 'blank.jpg'
            return None
        else:
            poster_image_url = image_prefix + poster_url

            # print(poster_image_url)
            data = requests.get(poster_image_url).content
            saved_img = 'img.jpg'
            
            f = open('img.jpg','wb')
            f.write(data)
            f.close()

        # img = Image.open('img.jpg')

        # img.show()




        img = cv2.imread(saved_img)
        height, width, channels = img.shape
        S_WIDTH, width, channels = img.shape
        # print("HEIHGT<", height, "WIDTH", width)
        box_height = 70
        
        if saved_img == 'blank.jpg':
            
            # bg_mask  = np.zeros_like(img, np.uint8)


            # x,y,w,h = 0,0,175,100

            # cv2.rectangle(bg_mask, (0, 0), (width, box_height), (255, 255, 255), cv2.FILLED)

            
            # out = img.copy()
            # alpha = 0.5
            # mask = bg_mask.astype(bool)
            # out[mask] = cv2.addWeighted(img, alpha, bg_mask, 1 - alpha, 0)[mask]

            # self.image = out
            # # Add text
            # cv2.putText(out, self.tvshow_name, (x + int(w/10),y + int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
            # self.add_buttons()
            self.image = img
            self.add_buttons()
            # cv2.imshow(self.tvshow_name, img)
            
        else:
            self.image = img
            self.add_buttons()
            # cv2.imshow(self.tvshow_name, img)
        
        k = cv2.waitKey(0)
        # print(k)
    

        if k == LIKED:
            self.add_liked()
            cv2.waitKey(SELECT_TIMER)
        if k == DIDNT_LIKE:
            self.add_didnt_like()
            cv2.waitKey(SELECT_TIMER)
        if k == WOULD_WATCH:
            self.add_would_watch()
            cv2.waitKey(SELECT_TIMER)
        if k == HAVENT_SEEN:
            self.add_havent_seen()
            cv2.waitKey(SELECT_TIMER)

        cv2.destroyAllWindows()

        return k
    
    def add_buttons(self):

      

        #### alpha, the 4th channel of the image
        alpha = 0.5

        overlay = self.image.copy()
        output = self.image.copy()


        #### apply the overlay
        

        cv2.circle(overlay,WOULD_WATCH_CENTER,BUTTON_RADIUS,BUTTON_COLOR,-1)
        cv2.putText(overlay,"watch",(WOULD_WATCH_CENTER[0]-65,WOULD_WATCH_CENTER[1]),cv2.FONT_HERSHEY_SIMPLEX,1.5,TEXT_COLOR,2)
        cv2.circle(overlay,HAVENT_SEEN_CENTER,BUTTON_RADIUS,BUTTON_COLOR,-1)
        cv2.putText(overlay,"X",(HAVENT_SEEN_CENTER[0]-10,HAVENT_SEEN_CENTER[1]),cv2.FONT_HERSHEY_SIMPLEX,1.5,TEXT_COLOR,2)
        cv2.circle(overlay,LIKED_CENTER,BUTTON_RADIUS,BUTTON_COLOR,-1)
        cv2.putText(overlay,"good",(LIKED_CENTER[0]-50,LIKED_CENTER[1]),cv2.FONT_HERSHEY_SIMPLEX,1.5,TEXT_COLOR,2)
        cv2.circle(overlay,DIDNT_LIKE_CENTER,BUTTON_RADIUS,BUTTON_COLOR,-1)
        cv2.putText(overlay,"bad",(DIDNT_LIKE_CENTER[0]-40,DIDNT_LIKE_CENTER[1]),cv2.FONT_HERSHEY_SIMPLEX,1.5,TEXT_COLOR,2)

        cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
        cv2.imshow(self.tvshow_name,output)
      
    
        # cv2.circle(self.image,WOULD_WATCH_CENTER,BUTTON_RADIUS,BUTTON_COLOR,BUTTON_THICKNESS)
        # cv2.putText(self.image,"looks good",WOULD_WATCH_CENTER,cv2.FONT_HERSHEY_SIMPLEX,1,BUTTON_COLOR)
        # cv2.circle(self.image,HAVENT_SEEN_CENTER,BUTTON_RADIUS,BUTTON_COLOR,BUTTON_THICKNESS)
        # cv2.putText(self.image,"unseen",HAVENT_SEEN_CENTER,cv2.FONT_HERSHEY_SIMPLEX,1,BUTTON_COLOR)
        # cv2.circle(self.image,LIKED_CENTER,BUTTON_RADIUS,BUTTON_COLOR,BUTTON_THICKNESS)
        # cv2.putText(self.image,"good",LIKED_CENTER,cv2.FONT_HERSHEY_SIMPLEX,1,BUTTON_COLOR)
        # cv2.circle(self.image,DIDNT_LIKE_CENTER,BUTTON_RADIUS,BUTTON_COLOR,BUTTON_THICKNESS)
        # cv2.putText(self.image,"bad",DIDNT_LIKE_CENTER,cv2.FONT_HERSHEY_SIMPLEX,1,BUTTON_COLOR)

        

    def add_liked(self):
        cv2.circle(self.image,LIKED_CENTER,BUTTON_RADIUS,LIKED_COLOR,SELECTED_THICKNESS)
        self.add_buttons()
        # cv2.imshow(self.tvshow_name, self.image)

    def add_didnt_like(self):
        cv2.circle(self.image,DIDNT_LIKE_CENTER,BUTTON_RADIUS,DIDNT_LIKE_COLOR,SELECTED_THICKNESS)
        self.add_buttons()
        # cv2.imshow(self.tvshow_name, self.image)
    
    def add_would_watch(self):
        cv2.circle(self.image,WOULD_WATCH_CENTER,BUTTON_RADIUS,WOULD_WATCH_COLOR,SELECTED_THICKNESS)
        self.add_buttons()
        # cv2.imshow(self.tvshow_name, self.image)

    def add_havent_seen(self):
        cv2.circle(self.image,HAVENT_SEEN_CENTER,BUTTON_RADIUS,HAVENT_SEEN_COLOR,SELECTED_THICKNESS)
        self.add_buttons()
        # cv2.imshow(self.tvshow_name, self.image)


# Call the function to get all TV shows
TV = TVWindow()
TV.get_all_tv_shows()

