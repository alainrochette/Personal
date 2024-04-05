from variables import *
import requests
from PIL import Image
import json
import numpy as np

import cv2


# 3 = right
# 2 = left
# 0 = up
# 1 = down
# 127 = backspace
# 48-57 = 0-9


url = "https://api.themoviedb.org/3/authentication"
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'
image_prefix = 'http://thetvdb.com/banners/'



url = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page=1&sort_by=popularity.desc&year=2023"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s"
}

class TVWindow():
        
    def __init__(self):
        self.image = None

    def get_all_tv_shows(self):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_key
        }
        response = requests.get(url, headers=headers)
        xNUM = 40000000
        
        YR = 2021
        if response.status_code == 200:
            page = 1
            total_show_i = 0

            url2 = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page={}&sort_by=popularity.desc&year={}}".format(page,YR)

            # url2 = "https://api.themoviedb.org/3/search/tv?query=a&first_air_date_year={}&include_adult=true&language=en-US&sort_by=primary_release_date.asc&watch_region=US&origin_country=US&page={}".format(str(YR),page) 
            # url2 = "https://api.themoviedb.org/3/search/tv?query=a&include_adult=true&language=en-US&sort_by=primary_release_date.asc&watch_region=US&origin_country=US&page={}".format(page) 


            response2 = requests.get(url2, headers=headers)
            
            # with open('data.json', 'w', encoding='utf-8') as f:
            #     json.dump(response2.json(), f, ensure_ascii=False, indent=4)
        
            num_pages = response2.json().get('total_pages', [])
            
            
            total_shows = 0 
            while page < num_pages:
                show_i = 0
                page = max(page,1)
                # print("page {} / {}".format(page, num_pages))
                url2 = "https://api.themoviedb.org/3/search/tv?query=a&first_air_date_year={}&include_adult=true&language=en-US&sort_by=primary_release_date.asc&watch_region=US&origin_country=US&page={}".format(str(YR),page) 
        
                # url2 = "https://api.themoviedb.org/3/search/tv?query=a&include_adult=true&language=en-US&sort_by=primary_release_date.asc&watch_region=US&origin_country=US&page={}".format(page) 
                response2 = requests.get(url2, headers=headers)
                tv_shows = response2.json().get('results', [])
                
                num_shows_in_page = len(tv_shows)
                
                if isReversed: 
                    tv_shows.reverse()
                    # isReversed = True
                # else:
                #     isReversed = False
                
                dir = 1
                # print(tv_shows)
                
                # for show in tv_shows:
                while show_i < num_shows_in_page and show_i >= 0:
                    show = tv_shows[show_i]
                    # total_shows += 1
                    self.tvshow_name = show.get('name', 'N/A')
                    
                    show_date = show.get('first_air_date', 'N/A')
                    orig_country = show.get('origin_country', 'N/A')
                    tvdb_id  = show.get('id')

                    if "US" in orig_country:
                        # print(show_name)
                        
                        total_show_i += 1
                        # print("show ",tvdb_id, show_i,"/",num_shows_in_page, "\n","Page:", page, "/",num_pages, show_name,show_date)
                        # show_i += 1
                        k = self.get_show_image(tvdb_id,total_show_i)
                        if k == EXIT:
                            break
                        if k != None:
                            dir = 0
                            if k == LEFT_ARROW:
                                dir = -1 if not isReversed else 1
                            if k == RIGHT_ARROW or k == WOULD_WATCH or k == HAVENT_SEEN or k == LIKED or k == DIDNT_LIKE:
                                dir = 1 if not isReversed else -1
                        # else:
                        #     dir = 1 if not isReversed else -1
                         

                        
                        # print(isReversed, dir)

                            # break
                    # else:
                        
                    # print('before',show_i)
                    show_i += dir
                    
                    # print('after',show_i)
                # if page > xNUM: break
                # print("next page")
                if k == EXIT:
                            break
                if show_i < 0: 
                    if isReversed:
                        page += 1
                        isReversed = False
                    else:
                        page -=1
                        if page >= 1 and not isReversed: 
                            isReversed = True
                        else:
                            isReversed = False
                    
                else:
                    if isReversed:

                        page -= 1
                        if page < 1: isReversed = False
                    else:
                        isReversed = False
                        page += 1

        else:
            print('Error retrieving TV shows:', response.text)

        print("TOTAL SHOWS", total_shows)

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

