import requests
from variables import * 

from MediaIcons import *

image_prefix = 'http://thetvdb.com/banners/'
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDdhYTc0YjliNjU1MGQ4OTEzOGUyMjllMmQ3MDVmNiIsInN1YiI6IjY0ODc4Yjg2ZTM3NWMwMDEzOWMxNjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.oSOmTVa06T10pA6I-RoFTH2okRbaEhRi_gECLMyIa9s'

class Person():
    def __init__(self,rawMedia,id):
        self.rawPerson = rawMedia
        self.id = id
        self.name = rawMedia['name'] if self.isTVShow else rawMedia["title"]
        