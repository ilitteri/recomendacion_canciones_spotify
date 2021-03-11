from graph import Graph, Edge, Vertex
from queue import Queue

def build_path(father: dict, origin: Vertex, destination: Vertex) -> list:
    w = origin.getLabel()
    v = destination.getLabel()
    path = []
    while v != w:
        path.append(v)
        v = father[v]
    path.append(w)
    return path[::-1]

def shortest_path(graph: Graph, origin: Vertex, destination: Vertex) -> tuple:
    visited = set()
    father = {}
    order = {}
    vertices = Queue()
    vertices.enqueue(origin)
    visited.add(origin.getLabel())
    father[origin.getLabel()] = None
    order[origin.getLabel()] = 0
    while not vertices.is_empty():
        v = vertices.dequeue()
        if v.getLabel() == destination.getLabel(): 
            break
        for w in v.getAdjacents():
            if w.getLabel() not in visited:
                visited.add(w.getLabel())
                father[w.getLabel()] = v.getLabel()
                order[w.getLabel()] = order[v.getLabel()] + 1
                vertices.enqueue(w)
    
    return order, father, visited

def central_vertices(users_graph: Graph, songs_graph: Graph, n: int) -> None:
    pass

def page_rank(users_graph: Graph, songs_graph: Graph, rec_type: str, n: int, songs: list) -> None:
    pass

def cycle(users_graph: Graph, songs_graph: Graph, n: int, song: str) -> None: # O(C^n)
    pass

def in_range(users_graph: Graph, songs_graph: Graph, n: int, song: str) -> None: # O(C+L)
    pass

def clustering_coefficient(users_graph: Graph, songs_graph: Graph, cancion: str = None) -> None:
    pass