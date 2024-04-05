from TVShow import TVShow
from Movie import Movie
import pickle
import json
from datetime import datetime
from datetime import timedelta
import requests

api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'

class Database():
    def __init__(self,menu):
        self.myDB = []
        self.menu = menu

        JOIN = False
        self.loadMyDB(JOIN)
        # self.cleanDB()
        # self.scrape()
        
    
    def cleanDB(self):
		# for mediaType in self.myDB:
		# i = 0
		# lenn = len(self.myDB["Movies"])
		# for media in self.myDB["Movies"][5000:]:
		# 	ss = sum(int(media.id) == int(x.id) for x in self.myDB["Movies"]) > 1
		# 	i += 1
		# 	print("{} / {}".format(i,lenn))
		# 	if ss:
		# 		self.myDB["Movies"].remove(media)
		# 		print("REMOVE", media.name, media.id)
		# 	else:
		# 		if media.imageUrl == None:
		# 			self.myDB["Movies"].remove(media)
        # for mediaType in self.myDB:
        #     for media in self.myDB[mediaType]:
        #         try:
        #             x = int(media.myRating)
        #         except:
        #             media.myRating = None
        i = 0
        nMovies = len(self.myDB["All Movies"]) + len(self.myDB["All TV Shows"])
        for movie in self.myDB["All Movies"]:
            self.addCrew(movie,True)
            i += 1
            print("{} / {}".format(i,nMovies))
            if i % 1000 == 0:
                self.saveMyDB()
            
        for show in self.myDB["All TV Shows"]:
            self.addCrew(show,False)
            i += 1
            print("{} / {}".format(i,nMovies))
            if i % 1000 == 0:
                self.saveMyDB()
        self.saveMyDB()
        

    def loadMyDB(self,join=False):
        # if join:
        #     dbfile = open('myDBMovies', 'rb')   
        #     myDBMovies = pickle.load(dbfile)
        #     dbfile.close()

        #     dbfile = open('myDBTVShows', 'rb')   
        #     myDBTVShows = pickle.load(dbfile)
        #     dbfile.close()
            
        #     newDB = {}
        #     newDB["All TV Shows"] = myDBTVShows
        #     newDB["All Movies"] = myDBMovies
        #     self.myDB = newDB
        #     self.saveMyDB()

        # else:
        dbfile = open('myDB', 'rb')   
        self.myDB = pickle.load(dbfile)
        
        dbfile.close()
      
    
    def idExists(self, id, movie=False):
        for media in self.myDB["All Movies" if movie else "All TV Shows"]:
            if int(media.id) == int(id):
                return media
        return False

    def personExists(self,id):
        if id in self.myDB["All People"]:
            return True
        return False
    

   
    
    def addTVShow(self,id,idInfo = None,personId=None):
        show = self.idExists(id,movie=False)
        if not show:
            if idInfo == None:
                newShow = TVShow(self.rawDB[id],id)
            else:
                newShow = TVShow(idInfo,id)
            if newShow.imageUrl != None:
                self.myDB["All TV Shows"].append(newShow)
                self.addCrew(newShow, movie = False, personID=personId)
                self.saveMyDB()
            return newShow
        elif personId:
            self.addCrew(show, movie=False, personID=personId)
        return show
    
    def addMovie(self,id, raw,personId=None):
        movie = self.idExists(id,movie=True)
        if not movie:
            newMovie = Movie(raw,id)
            if newMovie.imageUrl != None:
                self.myDB["All Movies"].append(newMovie)
                self.addCrew(newMovie, movie=True, personID=personId)
                self.saveMyDB()
            return newMovie
        elif personId:
            self.addCrew(movie, movie=True, personID=personId)
        return movie
    
    def addPerson(self, text):
        url = "https://api.themoviedb.org/3/search/person?query={}&include_adult=true&language=en-US&page=1".format(text.replace(" ","%20"))

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s"
        }
        response = requests.get(url, headers=headers)

        results = response.json()['results']
        ids = []
        for actor in results:
            if int(actor['id']) not in self.myDB["All People"]:
                self.myDB["All People"][int(actor['id'])] = actor['name']
            ids.append(actor['id'])
        return ids



    def addCrew(self,media,movie,personID):
        try:
            tst = media.castIDs
        except:
            media.castIDs = []
        if personID and personID not in media.castIDs:
            media.castIDs.append(personID)
        
        # if media.castIDs == []:
            
        try:
            x = self.myDB["All People"]
        except:
            self.myDB["All People"] = {}

        url = "https://api.themoviedb.org/3/{}/{}/credits?language=en-US".format("movie" if movie else "tv",media.id)
        


        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s"
        }
        

        response = requests.get(url, headers=headers)

        credits = response.json()

        if "cast" in credits:
            for member in credits['cast']:
                self.myDB["All People"][int(member['id'])] = member['name'] 
                if int(member['id']) not in media.castIDs:
                        media.castIDs.append(int(member['id']))

    def saveMyDB(self):
        for mediaType in self.myDB:
            for media in self.myDB[mediaType]:
                try:
                    media.unloadImg()
                except:
                    pass
        dbfile = open('myDB', 'wb')
        pickle.dump(self.myDB, dbfile)                   
        dbfile.close()

        # watchedList = list(filter(lambda x: x.watched, self.myDB["TV Shows"]))
        # for show in  list(sorted(watchedList, key=lambda x: x.name, reverse=False)):
        #     print("{} ({})".format(show.name,show.date[0:4]))
    
   
    
    
    def scrape(self):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_key
        }
        url = "https://api.themoviedb.org/3/authentication"
        response = requests.get(url, headers=headers)
        xNUM = 40000000
        
        
        if response.status_code == 200:
            
            for YR in range(1994,2024):
                print(YR)
                page = 1
                total_show_i = 0
            
                url2 = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page={}&sort_by=popularity.desc&year={}".format(page,YR)


                response2 = requests.get(url2, headers=headers)

                # print(response2.json())
                num_pages = int(response2.json().get('total_pages', []))
                # print("TOTAL PAGES",num_pages)
                
                MAXPAGES = 30 + YR - 1994
                while page < num_pages and page < MAXPAGES:
                    print("page {}/{} ({})".format(page,MAXPAGES,YR))
                    show_i = 0
                    page = max(page,1)
                    url2 = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page={}&sort_by=popularity.desc&year={}".format(page,YR)

                    response2 = requests.get(url2, headers=headers)
                    tv_shows = response2.json().get('results', [])
                    
                    num_shows_in_page = len(tv_shows)
                 
                    while show_i < num_shows_in_page and show_i >= 0:
                        show = tv_shows[show_i]
                        tvdb_id  = show.get('id')
                        orig_language = show.get('original_language', 'N/A')
                        if "en" in orig_language:
                            # print(show)
                            self.addMovie(tvdb_id,show)
                            total_show_i += 1
                       
                            
                        show_i += 1
                    page += 1
            # with open("allShows.json", "w") as outfile:
            #         json.dump(allShows, outfile   )

        else:
            print('Error retrieving Movies:', response.text)

        print("TOTAL Movies", len(self.myDB["All Movies"]))
# DB = Database()

# DB.loadDB()
# alph = sorted(DB.myDB, key=lambda x: x.name, reverse=False)
# for i in alph:
#     if "fboy" in i.name.lower():
#         print(i.name)
# for i in alph[0:100]:
    # print(i)
    # print(i.name)
# DB.loadMyDB()
    