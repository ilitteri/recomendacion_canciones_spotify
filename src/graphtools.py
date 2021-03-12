from graph import Graph
from queue import Queue

MIN_CYCLE_LENGTH: int = 3

def build_path(father: dict, origin: str, destination: str) -> list:
    w = origin
    v = destination
    path = []
    if w not in father:
        return None
    while v != w:
        path.append(v)
        v = father[v]
    path.append(w)
    return path[::-1]

def bfs_shortest_path(graph: Graph, origin: str, destination: str, visited: set = set()) -> list:
    father = {}
    vertices = Queue()
    vertices.enqueue(origin)
    visited.add(origin)
    father[origin] = None
    
    while not vertices.is_empty():
        v = vertices.dequeue()
        v_label = v
        if v_label == destination: 
            break
        for w in graph.adjacents(v):
            w_label = w
            if w_label not in visited:
                visited.add(w_label)
                father[w_label] = v_label
                vertices.enqueue(w)
    
    return build_path(father, origin, destination)

def central_vertices(users_graph: Graph, songs_graph: Graph, n: int) -> None:
    pass

def cycle_n(graph: Graph, origin: str, v: str, n: int, camino: list, visited: set = set()) -> bool:
    if n < MIN_CYCLE_LENGTH:
        return None
    if len(camino) == 0:
        camino.append(origin)
    visited.add(v)
    if len(camino) == n:
        return camino if origin in graph.adjacents(v) else None
    
    for w in graph.adjacents(v):
        if w in visited: continue
        solucion = cycle_n(graph, origin, w, n, camino + [w], visited)
        if solucion is not None:
            return solucion
    
    visited.remove(v)
    return None

def bfs_in_range(graph: Graph, origin: str, destination: int) -> tuple:
    songs_in_range = 0
    visited = set()
    order = {} # Para la distancia
    vertices = Queue()
    vertices.enqueue(origin)
    visited.add(origin)
    order[origin] = 0

    while not vertices.is_empty():
        v = vertices.dequeue()
        for w in graph.adjacents(v):
            if w not in visited:
                visited.add(w)
                order[w] = order[v] + 1
                if order[w] == destination: 
                    songs_in_range += 1
                if order[w] > destination:
                    break
                vertices.enqueue(w)
    return songs_in_range

def clustering(graph: Graph, v: str) -> float:
    adjacents = graph.adjacents(v)
    if len(adjacents) < 2:
        return round(0, 3)
    
    edgeCount = 0

    for w in adjacents:
        for x in adjacents:
            if w != x:
                if graph.are_joined(x, w) and x != w:
                    edgeCount += 1

    v_out_degree = len(adjacents)

    return round(edgeCount / (v_out_degree * (v_out_degree - 1)), 3) 

def pagerank(graph: Graph, v: str, most_importants: dict, iterations: int = 20, d: float = 0.85):
    degree = graph.order()
    for _ in range(iterations):
        for v in graph:
            most_importants[v] = (1 - d) / degree + d * sum(most_importants[w] / len(graph.adjacents(w)) for w in graph.adjacents(v))