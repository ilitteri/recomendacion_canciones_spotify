#!/usr/bin/python3
import sys
import tsv_reader
import load_structures
from graph import Graph
from constants import *
from error_messages import *
from error_handling import parameters_error_handler, command_handle_error, input_handle_error, path_handle_error
from recomendicommands import get_cycle_n, load_most_importants, recommend, walk, in_range, print_clustering_coefficient, print_song_list

def process_stdin(users_graph: Graph, songs: dict, users: dict, playlists: dict) -> None:
    '''
    Procesa la entrada por consola:
    Va leyendo la entrada y parseandola para la ejecucion de comandos.
    '''
    most_importants = []
    songs_graph = None
    stdin = sys.stdin.readline().rstrip('\n')
    while stdin:
        if len(stdin) > 0:
            stdin = stdin.split(maxsplit=1)
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
            walk(users_graph, songs, origin, destination)
        elif command == MOST_IMPORTANTS:
            parameters = stdin[1].split()
            if not parameters_error_handler(command, MOST_IMPORTANTS_PARAMETER_COUNT, parameters):
                continue
            if len(most_importants) == 0:
                most_importants = load_most_importants(users_graph, songs)
            print_song_list(most_importants, int(parameters[0]))
        elif command == RECOMENDATION:
            parameters = stdin[1].split(maxsplit=2)
            if not parameters_error_handler(command, RECOMENDATION_PARAMETER_COUNT, parameters):
                continue
            rec_type, n, liked_songs = parameters
            liked_songs = liked_songs.split(' >>>> ')
            recommended = recommend(users_graph, users, songs, rec_type, liked_songs)
            print_song_list(recommended, int(n))
        elif command == CYCLE:
            if songs_graph == None:
                songs_graph = load_structures.load_playlists_song_structure(playlists, songs)
            parameters = stdin[1].split(maxsplit=1)
            if not parameters_error_handler(command, CYCLE_PARAMETER_COUNT, parameters):
                continue
            n, song = parameters
            get_cycle_n(songs_graph, song, int(n))
        elif command == RANGE:
            if songs_graph == None:
                songs_graph = load_structures.load_playlists_song_structure(playlists, songs)
            parameters = stdin[1].split(maxsplit=1)
            if not parameters_error_handler(command, RANGE_PARAMETER_COUNT, parameters):
                continue
            n, song = parameters
            in_range(songs_graph, int(n), song)
        elif command == CLUSTERING:
            if songs_graph == None:
                songs_graph = load_structures.load_playlists_song_structure(playlists, songs)
            print_clustering_coefficient(songs_graph, None if len(stdin) == 1 else stdin[1])
        stdin = sys.stdin.readline().rstrip('\n')

def main():
    '''
    Funcion principal que ejecuta la aplicacion
    '''
    parsed_lines = tsv_reader.read_input(sys.argv[1])
    songs, users, playlists, user_song = load_structures.load_data(parsed_lines)
    process_stdin(user_song, songs, users, playlists)

if __name__ == '__main__':
    main()
