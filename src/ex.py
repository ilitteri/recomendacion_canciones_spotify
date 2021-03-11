from queue import Queue
from graph import Graph, Vertex, Edge

MIN_CYCLE_LENGTH = 3

def bfs_in_range(graph: Graph, origin: Vertex, destination: int, visited: set, order: dict) -> tuple:
    songs_in_range = 0
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
        out += f'{v0} --> aparece en playlist --> {v0v1} --> de --> {v1} --> tiene una playlist --> {v1v2} --> donde aparece --> '
        i += 2
    out += v2
    print(out)

def build_path(father: dict, origin: Vertex, destination: Vertex) -> list:
  v = destination.getLabel()
  path = []
  while v != origin.getLabel():
    path.append(v)
    v = father[v]
  path.append(origin.getLabel())
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

def print_cycle(songs_graph: Graph, cycle: list) -> None:
    out = ""
    for v in cycle[:-1]:
        out += f'{v} --> '
    out += cycle[-1]
    print(out)

def main():
    graph = Graph()
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")
    f = Vertex("F")
    g = Vertex("G")
    h = Vertex("H")
    i = Vertex("I")
    j = Vertex("J")
    graph.addVertex(a)
    graph.addVertex(b)
    graph.addVertex(c)
    graph.addVertex(d)
    graph.addVertex(e)
    graph.addVertex(f)
    graph.addVertex(g)
    graph.addVertex(h)
    graph.addVertex(i)
    graph.addVertex(j)

    graph.addEdge(Edge(a, b))
    graph.addEdge(Edge(a, d))
    graph.addEdge(Edge(a, c))
    graph.addEdge(Edge(a, i))
    graph.addEdge(Edge(b, d))
    graph.addEdge(Edge(e, f))
    graph.addEdge(Edge(f, g))
    graph.addEdge(Edge(g, h))
    graph.addEdge(Edge(h, i))
    graph.addEdge(Edge(c, e))
    graph.addEdge(Edge(e, g))
    for i in range(3, 10):
        cycle = n_cycle(graph, a, a, i, [], set())
        if cycle is not None:
            cycle.append(a.getLabel())
            print_cycle(graph, cycle)

    # In Range Test
    # graph.addEdge(Edge(a, b))
    # graph.addEdge(Edge(a, c))
    # graph.addEdge(Edge(a, d))
    # graph.addEdge(Edge(b, e))
    # graph.addEdge(Edge(b, i))
    # graph.addEdge(Edge(c, f))
    # graph.addEdge(Edge(c, j))
    # graph.addEdge(Edge(d, g))
    # graph.addEdge(Edge(d, h))
    # songs = bfs_in_range(graph, a, 2, set(), {})
    # print(songs)

    # Shortest Path Test
    # graph.addEdge(Edge(a, e))
    # graph.addEdge(Edge(a, f))
    # graph.addEdge(Edge(b, f))
    # graph.addEdge(Edge(b, g))
    # graph.addEdge(Edge(c, g))
    # graph.addEdge(Edge(c, h))
    # graph.addEdge(Edge(d, h))
    # _, father, _, = shortest_path(graph, e, h)
    # print(build_path(father, e, h))
    # print_shortest_path(graph, build_path(father, e, h))

main()