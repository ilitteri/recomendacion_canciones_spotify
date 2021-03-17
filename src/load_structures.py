from graph import Graph
from constants import VALUES_COUNT
from user import User
from playlist import Playlist
from song import Song

def load_playlists_song_structure(playlists: dict, songs: dict) -> Graph:
    '''
    Crea un grafo no dirigido relacionando canciones si aparecen en una misma
    playlist (al menos una playlist lista a ambas canciones).
        Pre: se leyo el archivo y se cargaron las playlist con sus canciones.
        Pos: grafo no dirigido relacionando canciones que aparecen en una misma
            playlist.
    '''
    graph = Graph(is_directed=False)

    for song in songs:
        graph.add_vertex(song)

    for playlist in playlists:
        for song1 in playlists[playlist]:
            for song2 in playlists[playlist]:
                if not graph.are_joined(song1, song2) and song1 != song2:
                    graph.add_edge(song1, song2, (playlists[playlist].getOwner(), playlist))
    return graph

def load_data(lines: list) -> tuple:
    '''
    Carga los datos del dataset en estructuras.
        Pre: se leyo el dataset y se parsearon las lineas en una lista.
        Pos: se devuelve una tupla con las estructuras: canciones, usuarios,
            playlists, y un grafo no dirigido que relaciona si a un usuario le
            gusta una cancion.
    '''
    songs = {}
    users = {}
    playlists = {}
    graph = Graph(is_directed=False)

    for line in lines:
        if len(line) != VALUES_COUNT:
            continue
        _, user_id, track_name, artist, playlist_id, playlist_name, genres = line
        if playlist_name not in playlists:
            playlists[playlist_name] = Playlist(playlist_id, playlist_name, user_id)
        song_tag = track_name+" - "+artist
        if song_tag not in songs:
            song = Song(song_tag, artist, genres.split(','))
            songs[song_tag] = song
        playlists[playlist_name].addSong(songs[song_tag])
        if user_id not in graph:
            users[user_id] = User(user_id)
            graph.add_vertex(user_id)
        if song_tag not in graph:
            graph.add_vertex(song_tag)
        if not graph.are_joined(user_id, song_tag):
            graph.add_edge(user_id, song_tag, playlist_name)

    return songs, users, playlists, graph
