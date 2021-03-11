#!/usr/bin/python3
import os
import sys
from graph import Graph, Edge, Vertex
from user import User
from playlist import Playlist
from song import Song
from constants import *
from errors import *
from recomendicommands import get_n_cycle, walk, in_range

def path_handle_error(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError("Buscate un archivo de verdad.")

def read_input(path: str) -> list:
    '''Lee el archivo de entrada y lo parsea.'''
    path_handle_error(path)
    parsed_lines = []
    with open(path, "r") as input_file:
        line = input_file.readline().rstrip('\n') # Header
        line = input_file.readline().rstrip('\n')
        while line:
            parsed_lines.append(line.split('\t'))
            line = input_file.readline().rstrip('\n')

    return parsed_lines

def input_handle_error(line: str) -> bool:
    '''
    Verifica que la entrada por consola sea valida.
    Pre: se ingreso por consola.
    '''
    line = line.split(maxsplit=1)
    if len(line) < 1:
        print(ERROR_INPUT)
        return False
    elif len(line) == 1:
        if CLUSTERING in line:
            return True
        else:
            print(ERROR_PARAM_COUNT)
            return False
    return True

def command_handle_error(command: str) -> bool:
    '''
    Verifica que el comando ingresado sea valido.
    Pre: se verifico el ingreso por consola.
    '''
    if command in COMMANDS:
        print(ERROR_CMD)
        return False
    return True

def parameters_handle_error(command: str, n: int = 0, *parameters: tuple) -> bool:
    '''
    Verifica que la cantidad de parametros sea valida para cada comando.
    Pre: se verifico el ingreso por consola.
    '''
    if command != CLUSTERING:
        return len(parameters) == n
    return not (len(parameters) > n)    

def load_playlists_song_structure(playlists: dict, songs: dict) -> Graph:
    graph = Graph()

    for song in songs:
        graph.addVertex(Vertex(song, songs[song], SONG_COLOR))

    for playlist in playlists:
        added = {}
        for song1 in playlists[playlist]:
            added[song1] = True
            for song2 in playlists[playlist]:
                if not (song1 in added and song2 in added):
                    graph.addEdge(Edge(graph.getVertex(song1), graph.getVertex(song2), (playlists[playlist].getOwner(), playlist)))
    
    return graph

def load_user_song_structure_(lines: list) -> Graph:
    '''
    Lee las lineas parseadas y carga en memoria los datos.
    Pre: Un archivo fue leido y parseado.
    '''
    graph = Graph()
    for line in lines:
        _, user_id, track_name, artist, playlist_id, playlist_name, genres = line
        user = Vertex(user_id, color=USER_COLOR)
        song = Vertex(track_name+" - "+artist, color=SONG_COLOR)
        graph.addVertex(user)
        graph.addVertex(song)
        graph.addEdge(Edge(user, song, ))

    return graph

def process_stdin(users_graph: Graph, songs_graph: Graph) -> None:
    while True:
        stdin = input('')
        if not input_handle_error(stdin): continue
        command, parameters = stdin.split(maxsplit=1)
        if not command_handle_error(command): continue
        if command == WALK:
            origin, destination = parameters.split('>>>>')
            if not parameters_handle_error(command, WALK_PARAMETERS_COUNT, origin, destination): continue
            walk(users_graph, songs_graph, origin, destination)
        # elif command == MOST_IMPORTANTS:
        #     if not parameters_handle_error(command, MOST_IMPORTANTS_PARAMETER_COUNT, parameters): continue
        #     central_vertices(songs_graph, parameters)

        # elif command == RECOMENDATION:
        #     rec_type, n, songs = parameters.split(maxsplit=2)
        #     songs = songs.split('>>>>')
        #     if not parameters_handle_error(command, RECOMENDATION_PARAMETER_COUNT, rec_type, n, songs):
        #         continue
        #     page_rank(graph, rec_type, n, songs)
        elif command == CYCLE:
            n, song = parameters.split(maxsplit=1)
            if not parameters_handle_error(command, CYCLE_PARAMETER_COUNT, n, song):
                continue
            get_n_cycle(songs_graph, song, n)
        elif command == RANGE:
            n, song = parameters.split(maxsplit=1)
            if not parameters_handle_error(command, RANGE_PARAMETER_COUNT, n, song):
                continue
            in_range(songs_graph, int(n), song)
        # elif command == CLUSTERING:
        #

def load_data(lines: list) -> tuple:
    songs = {}
    graph = Graph()
    playlists = {}
    for line in lines:
        _, user_id, track_name, artist, playlist_id, playlist_name, genres = line
        # if user_id not in users:
        #     users[user_id] = User(user_id)
        if playlist_id not in playlists:
            playlists[playlist_id] = Playlist(playlist_id, playlist_name, user_id)
        # if playlist_id not in users[user_id]:
        #     users[user_id].addPlaylist(playlists[playlist_id])
        song_tag = track_name+" - "+artist
        if song_tag not in songs:
            song = Song(song_tag, artist, genres.split(','))
            songs[song_tag] = song
            playlists[playlist_id].addSong(song)
            # user_playlist = users[user_id].getPlaylists()[playlist_id]
            # user_playlist.addSong(song)

        user = Vertex(user_id, color=USER_COLOR)
        song = Vertex(song_tag, color=SONG_COLOR)
        graph.addVertex(user)
        graph.addVertex(song)
        graph.addEdge(Edge(user, song, playlists[playlist_id]))

    return songs, playlists, graph

def main():
    parsed_lines = read_input(sys.argv[1])
    songs, playlists, users = load_data(parsed_lines)
    songs = load_playlists_song_structure(playlists, songs)
    process_stdin(users, songs)

if __name__ == '__main__':
    main()