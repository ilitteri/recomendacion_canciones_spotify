from constants import SONG_COLOR, USER_COLOR
from ex import build_path
from graph import Graph, Edge, Vertex
from graphtools import shortest_path, central_vertices, page_rank, cycle, clustering_coefficient, in_range

def print_shortest_path(users_graph: Graph, path: list) -> None:
    out = ""
    v0v1 = v1v2 = "playlist"
    vertices = users_graph.getVertices()
    i = 2
    v0 = v1 = v2 = None
    while i < len(path):
        v0 = path[i-2]
        v1 = path[i-1]
        v2 = path[i]
        e01 = users_graph.getEdge(users_graph(v0), users_graph(v1))
        e12 = users_graph.getEdge(users_graph(v1), users_graph(v2))
        out += f'{v0} --> aparece en playlist --> {e01} --> de --> {v1} --> tiene una playlist --> {e12} --> donde aparece --> '
        i += 2
    out += v2
    print(out)

def walk(users_graph: Graph, origin: str, destination: str) -> None:
    _, father, _ = shortest_path(users_graph, origin, destination)
    path = build_path(father, origin.getLabel(), destination.getLabel())
    print_shortest_path(users_graph, path)