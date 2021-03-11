from typing_extensions import TypeVarTuple
from graph import Graph, Edge, Vertex
from queue import Queue

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

def bfs_cycle(graph: Graph, v: Vertex, n: int, visited: set = set()):
  vertices = Queue()
  vertices.enqueue(v)
  visited.add(v.getLabel())
  father = {}  # Para poder reconstruir el ciclo
  father[v.getLabel()] = None

  while not vertices.is_empty():
    v = vertices.dequeue()
    v_label = v.getLabel()
    for w in v.getAdjacents():
        w_label = w.getLabel()
        if w_label in visited:
            if w_label != father[v_label]:
                return build_path(father, w, v)
        else:
            vertices.enqueue(w)
            visited.add(v_label)
            father[w_label] = v_label

def cycle_n(graph: Graph, origin: Vertex, v: Vertex, n: int, camino: list, visited: set = set()) -> bool:
    visited.add(v)
    camino.append(v)
    if len(camino) == n and v == origin: # Si ya encontre solucion 
        return True
    if len(camino) == n and v != origin: # Retrocede
        visited.remove(v)
        camino.remove(v)
        return False

    for w in v.getAdjacents(): 
        if w not in visited:
            visited.add(w)
            camino.append(w)
            if len(camino) == n and w != origin: # Retrocede
                visited.remove(w)
                camino.remove(w)
                continue
            elif n_cycle(graph, origin, w, n, camino, visited):
                return True

    visited.remove(v)
    camino.remove(v)
    return False

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