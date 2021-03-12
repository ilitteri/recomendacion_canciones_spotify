class Song:
    '''Estructura que almacena datos de una cancion'''
    def __init__(self, name: str, artist: str, genres: list) -> None:
        self.__name = name
        self.__artist = artist
        self.__genres = genres
    
    def getGenre(self) -> str:
        return self.__genre
    
    def getName(self) -> str:
        return self.__name

    def getArtist(self) -> str:
        return self.__artist

    def getGenres(self) -> list:
        return self.__genres