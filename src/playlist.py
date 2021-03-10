from typing import Dict, Iterator
from song import Song

class Playlist:
    def __init__(self, id: str, name: str, songs: dict = None) -> None:
        self.__id = id
        self.__name = name
        self.__songs = songs or {}
    
    def __iter__(self) -> Iterator:
        return iter(self.__songs)
    
    def __contains__(self, trackName: str) -> bool:
        return trackName in self.__songs
    
    def __len__(self) -> int:
        return len(self.__songs)

    def getID(self) -> str:
        return self.__id
    
    def getName(self) -> str:
        return self.__name

    def getSongs(self) -> dict:
        return self.__songs
    
    def addSong(self, song: Song) -> None:
        name = song.getName()
        self.__songs[name] = Song
    
    def removeSong(self, song: Song) -> None:
        name = song.getName()
        if name in self.__songs:
            del(self.__songs[name])