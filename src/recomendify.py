#!/usr/bin/python3
import sys
from graph import Graph
from user import User
from playlist import Playlist
from song import Song
from constants import *
from error_messages import *
from error_handling import parameters_error_handler, command_handle_error, input_handle_error, path_handle_error, recomendation_parameter_error_handler
from recomendicommands import get_cycle_n, load_most_importants, recommend, walk, in_range, print_clustering_coefficient, print_song_list

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

def load_playlists_song_structure(playlists: dict, songs: dict) -> Graph:
    graph = Graph(is_directed=False)

    for song in songs:
        graph.add_vertex(song)

    for playlist in playlists:
        for song1 in playlists[playlist]:
            for song2 in playlists[playlist]:
                if not graph.are_joined(song1, song2) and song1 != song2:
                    graph.add_edge(song1, song2, (playlists[playlist].getOwner(), playlist)) 
    return graph

def process_stdin(users_graph: Graph, songs_graph: Graph, songs: dict, users: dict) -> None:
    most_importants = []
    while True:
        stdin = input('').split(maxsplit=1)
        if not input_handle_error(stdin): 
            continue
        command = stdin[0]
        if not command_handle_error(command): 
            continue
        if command == WALK:
            parameters = stdin[1].split(' >>>> ')
            if not parameters_error_handler(command, WALK_PARAMETERS_COUNT, parameters): 
                continue
            origin, destination = parameters
            walk(users_graph, origin, destination)
        elif command == MOST_IMPORTANTS:
            parameters = stdin[1].split()
            if not parameters_error_handler(command, MOST_IMPORTANTS_PARAMETER_COUNT, parameters): 
                continue
            if len(most_importants) == 0:
                most_importants = load_most_importants(users_graph, songs)
            print_song_list(most_importants, int(parameters[0]))

        elif command == RECOMENDATION:
            rec_type, n, liked_songs = stdin[1].split(maxsplit=2)
            liked_songs = liked_songs.split(' >>>> ')
            # if not parameters_error_handler(command, RECOMENDATION_PARAMETER_COUNT, rec_type, n, songs):
            #     continue
            recommended = recommend(users_graph, users, songs, rec_type, liked_songs)
            print_song_list(recommended, int(n))

        elif command == CYCLE:
            parameters = stdin[1].split(maxsplit=1)
            if not parameters_error_handler(command, CYCLE_PARAMETER_COUNT, parameters):
                continue
            n, song = parameters
            get_cycle_n(songs_graph, song, int(n))
        elif command == RANGE:
            parameters = stdin[1].split(maxsplit=1)
            if not parameters_error_handler(command, RANGE_PARAMETER_COUNT, parameters):
                continue
            n, song = parameters
            in_range(songs_graph, int(n), song)
        elif command == CLUSTERING:
            # if not parameters_error_handler(command, CLUSTERING_PARAMETER_COUNT, ):
            #     continue
            print_clustering_coefficient(songs_graph, None if len(stdin) == 1 else stdin[1])

def load_data(lines: list) -> tuple:
    songs = {}
    users = {}
    playlists = {}
    graph = Graph(is_directed=False)

    for line in lines:
        _, user_id, track_name, artist, playlist_id, playlist_name, genres = line
        if playlist_id not in playlists:
            playlists[playlist_id] = Playlist(playlist_id, playlist_name, user_id)
        song_tag = track_name+" - "+artist
        if song_tag not in songs:
            song = Song(song_tag, artist, genres.split(','))
            songs[song_tag] = song
        playlists[playlist_id].addSong(songs[song_tag])
        
        if user_id not in graph:
            users[user_id] = User(user_id)
            graph.add_vertex(user_id)
        if song_tag not in graph:
            graph.add_vertex(song_tag)
        if not graph.are_joined(user_id, song_tag):
            graph.add_edge(user_id, song_tag, playlist_name)

    return songs, users, playlists, graph

def main():
    parsed_lines = read_input(sys.argv[1])
    songs, users, playlists, user_song = load_data(parsed_lines)
    songs_g = load_playlists_song_structure(playlists, songs)
    process_stdin(user_song, songs_g, songs, users)

if __name__ == '__main__':
    main()