from Media import *

class Movie(Media):
    def __init__(self,rawShow,id):
        super().__init__(rawShow,id,"Movie")
        