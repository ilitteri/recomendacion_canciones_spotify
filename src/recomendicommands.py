from errors import *
from graph import Graph
from graphtools import bfs_shortest_path, bfs_in_range, cycle_n, clustering, pagerank

def error_handler(element: list, msg: str) -> bool:
    if element == None:
        print(msg)
        return False
    return True

def end_points_error_handler(users_graph: Graph, origin: str, destination: str) -> bool:
    if origin not in users_graph or destination not in users_graph:
        print(ERROR_INVALID_SONG)
        return False
    return True

def print_shortest_path(users_graph: Graph, path: list) -> None:
    out = ""
    i = 2
    v0 = v1 = v2 = None
    while i < len(path):
        v0 = path[i-2]
        v1 = path[i-1]
        v2 = path[i]
        e01 = users_graph.edge_weight(v0, v1)
        e12 = users_graph.edge_weight(v1, v2)
        out += f'{v0} --> aparece en playlist --> {e01} --> de --> {v1} --> tiene una playlist --> {e12} --> donde aparece --> '
        i += 2
    out += v2
    print(out)

def walk(users_graph: Graph, origin: str, destination: str) -> None:
    if not end_points_error_handler(users_graph, origin, destination): 
        return
    path = bfs_shortest_path(users_graph, origin, destination)
    if not error_handler(path, ERROR_PATH_NOT_FOUND):
        return
    print_shortest_path(users_graph, path)

def song_error_handler(songs_graph: Graph, song: str) -> bool:
    if song not in songs_graph:
        print(ERROR_SONG)
        return False
    return True

def print_cycle(cycle: list) -> None:
    out = ""
    for v in cycle:
        out += f'{v} --> '
    out += cycle[0]
    print(out)

def get_cycle_n(songs_graph: Graph, song: str, n: int) -> None:
    cycle = cycle_n(songs_graph, song, song, n, [], set())
    if not error_handler(cycle, ERROR_CYCLE): 
        return
    print_cycle(cycle)

def in_range(songs_graph: Graph, n: int, song: str) -> None: # O(C+L)
    if not song_error_handler(songs_graph, song): 
        return
    songs_in_range = bfs_in_range(songs_graph, song, n)
    print(songs_in_range)

def print_clustering_coefficient(songs_graph: Graph, song: str = None) -> None:
    if song == None:
        print(round(sum(clustering(songs_graph, v) for v in songs_graph) / songs_graph.order(), 3))
    else: 
        print(clustering(songs_graph, song))

def print_most_importants(most_importants: list, n: int) -> None:
    out = ""
    i = 0
    for _, song in most_importants:
        if i == n:
            break
        out += f'{song}{"; " if song != most_importants[n-1][1] else ""}'
        i += 1
    print(out)

def initialize_pagerank(graph: Graph, d: float = 0.85) -> dict:
    initial_ranks = {}
    for v in graph:
        initial_ranks[v] = (1 - d) / graph.order()
    return initial_ranks

def sort_most_importants(songs: dict, most_importants: dict):
    return sorted([(most_importants[v], v) for v in most_importants if v in songs])

def load_most_importants(users_graph: Graph, songs: dict) -> list:
    initial_ranks = initialize_pagerank(users_graph)
    pagerank(users_graph, users_graph.random_vertex(), initial_ranks)
    return sort_most_importants(songs, initial_ranks)