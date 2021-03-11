from typing_extensions import TypeVarTuple
from graph import Graph, Edge, Vertex
from queue import Queue

MIN_CYCLE_LENGTH = 3

def build_path(father: dict, origin: Vertex, destination: Vertex) -> list:
    w = origin.getLabel()
    v = destination.getLabel()
    path = []
    if w not in father:
        return None
    while v != w:
        path.append(v)
        v = father[v]
    path.append(w)
    return path[::-1]

def bfs_shortest_path(graph: Graph, origin: Vertex, destination: Vertex, visited: set = set()) -> list:
    father = {}
    vertices = Queue()
    vertices.enqueue(origin)
    origin_label = origin.getLabel()
    visited.add(origin_label)
    father[origin_label] = None
    
    while not vertices.is_empty():
        v = vertices.dequeue()
        v_label = v.getLabel()
        if v_label == destination.getLabel(): 
            break
        for w in v.getAdjacents():
            w_label = w.getLabel()
            if w_label not in visited:
                visited.add(w_label)
                father[w_label] = v_label
                vertices.enqueue(w)
    
    return build_path(father, origin, destination)

def central_vertices(users_graph: Graph, songs_graph: Graph, n: int) -> None:
    pass

def page_rank(users_graph: Graph, songs_graph: Graph, rec_type: str, n: int, songs: list) -> None:
    pass

def n_cycle(graph: Graph, origin: Vertex, v: Vertex, n: int, camino: list, visited: set = set()) -> bool:
    if n < MIN_CYCLE_LENGTH:
        return None
    if len(camino) == 0:
        camino.append(origin.getLabel())
    visited.add(v.getLabel())
    if len(camino) == n:
        return camino if origin in v.getAdjacents() else None
    
    for w in v.getAdjacents():
        if w.getLabel() in visited: continue
        solucion = n_cycle(graph, origin, w, n, camino + [w.getLabel()], visited)
        if solucion is not None:
            return solucion
    
    visited.remove(v.getLabel())
    return None

def bfs_in_range(graph: Graph, origin: Vertex, destination: int, visited: set = set()) -> tuple:
    songs_in_range = 0
    order = {} # Para la distancia
    vertices = Queue()
    vertices.enqueue(origin)
    visited.add(origin.getLabel())
    order[origin.getLabel()] = 0

    while not vertices.is_empty():
        v = vertices.dequeue()
        if order[v.getLabel()] == destination: 
            songs_in_range += 1
        if order[v.getLabel()] > destination:
            break
        for w in v.getAdjacents():
            if w.getLabel() not in visited:
                visited.add(w.getLabel())
                order[w.getLabel()] = order[v.getLabel()] + 1
                vertices.enqueue(w)
    return songs_in_range

def clustering_coefficient(users_graph: Graph, songs_graph: Graph, cancion: str = None) -> None:
    pass