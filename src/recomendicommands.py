from constants import SONG_COLOR, USER_COLOR
from errors import ERROR_INVALID_SONG, ERROR_PATH_NOT_FOUND
from graph import Graph, Edge, Vertex
from graphtools import shortest_path, central_vertices, page_rank, cycle, clustering_coefficient, in_range, build_path

def end_points_error_handler(users_graph: Graph, origin: str, destination: str) -> bool:
    if origin not in users_graph or destination not in users_graph:
        print(ERROR_INVALID_SONG)
        return False
    return True

def path_error_handler(visited: dict, destination: str) -> bool:
    if destination not in visited:
        print(ERROR_PATH_NOT_FOUND)
        return False
    return True

def print_shortest_path(users_graph: Graph, path: list) -> None:
    out = ""
    vertices = users_graph.getVertices()
    i = 2
    v0 = v1 = v2 = None
    while i < len(path):
        v0 = path[i-2]
        v1 = path[i-1]
        v2 = path[i]
        e01 = users_graph.getEdge(vertices[v0], vertices[v1])
        e12 = users_graph.getEdge(vertices[v1], vertices[v2])
        out += f'{v0} --> aparece en playlist --> {e01} --> de --> {v1} --> tiene una playlist --> {e12} --> donde aparece --> '
        i += 2
    out += v2
    print(out)

def walk(users_graph: Graph, origin: str, destination: str) -> None:
    if not end_points_error_handler(users_graph, origin, destination): 
        return
    _, father, visited = shortest_path(users_graph, origin, destination)
    if not path_error_handler(visited):
        return
    path = build_path(father, origin.getLabel(), destination.getLabel())
    print_shortest_path(users_graph, path)