from typing import Iterator
from playlist import Playlist

class User:
    '''Estructura que almacena datos de usuario'''
    def __init__(self, name: str, playlists: dict = None) -> None:
        self.__name = name
        self.__playlists = playlists or {}

    def __contains__(self, playlistID: str) -> bool:
        return playlistID in self.__playlists

    def __iter__(self) -> Iterator:
        return iter(self.__playlists)

    def getName(self) -> str:
        return self.__name
    
    def getPlaylists(self) -> str:
        return self.__playlists
    
    def addPlaylist(self, playlist: Playlist):
        id = playlist.getID()
        if id not in self.__playlists:
            self.__playlists[id] = playlist

    def removePlaylist(self, playlist: Playlist):
        id = playlist.getID()
        if id not in self.__playlists:
            del(self.__playlists[id])