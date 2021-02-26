class Vertex:
    def __init__(self, label: str):
        self.label = label
        # self.eccentricity = None #se asume el vertice aislado
        self.adjacents = set()
        self.incidentEdges = set()
    
    def __str__(self):
        return f'{self.label}'
    
    def __iter__(self):
        return iter(self.adjacents)

    def getLabel(self) -> str:
        return self.label
    
    def getDegree(self) -> int:
        return len(self.incidentEdges)
    
    # def getEccentricity(self) -> float:
    #     return self.eccentricity if self.eccentricity != None else float('inf')

    def getAdjacents(self) -> set:
        return self.adjacents
    
    def isAdjacentOf(self, other) -> bool:
        return other in self.adjacents
    
    def getAdjacentsCount(self) -> int:
        return len(self.adjacents)
    
    def isIsolated(self) -> bool:
        return len(self.adjacents) == 0 and len(self.incidentEdges) == 0

    def addAdjacent(self, other) -> None:
        self.adjacents.add(other)
    
    def addIncidentEdge(self, edge) -> None:
        self.incidentEdges.add(edge)

class Edge:
    def __init__(self, v1, v2):
        self.endPoints = set([v1, v2])

    def __iter__(self):
        return iter(self.endPoints)
    
    def __str__(self):
        return f'{self.endPoints[0]}<--->{self.endPoints[1]}'

    def getEndPoints(self) -> set:
        return self.endPoints
    
    def isLoop(self) -> bool:
        return self.endPoints[0] == self.endPoints[1]
        
class Graph:
    def __init__(self, verticesSet: dict = None, edgesSet: set = None, isDigraph: bool = False):
        self.verticesSet = verticesSet or {}
        self.edgesSet = edgesSet or set()
        self.isDigraph = isDigraph

        self.radius = None
        self.diameter = None
        self.center = set()
        self.periphery = set()
        self.verticesEccentricities = {}
        self.verticesDegrees = {}

        self._dirty = False
    
    def __iter__(self):
        return iter(self.verticesSet)
    
    def __contains__(self, vertex):
        return vertex in self.verticesSet
    
    def __len__(self):
        return len(self.verticesSet)
    
    def __add__(self, other):
        return Graph({**self.verticesSet, **other.verticesSet}, self.edgesSet+other.edgesSet)
        #Py3.9#return Graph(self.verticesSet | other.verticesSet, self.edgesSet+other.edgesSet)

    def isConnected(self) -> bool:
        if len(self.verticesSet) == 0:
            return True
        visited = set()
        q = []
        origin = self.verticesSet.values()[0]
        visited.add(origin)
        q.append(origin)
        while len(q) != 0:
            vertex = q.pop(0)
            for adjacent in vertex.getAdjacents():
                if not adjacent in visited:
                    visited.add(adjacent)
                    q.append(adjacent)
        return self.verticesSet == visited

    def update(self) -> None:
        self.verticesDegrees.update({vertex.getLabel():vertex.getDegree() for vertex in self})
        if self.isConnected():
            self.verticesEccentricities.update({vertex.getLabel():self.getEccentricityOf(vertex) for vertex in self})
            verticesEccentricities = self.verticesEccentricities.values()
            self.radius = min(verticesEccentricities)
            self.diameter = max(verticesEccentricities)
            self.center = list(filter(min, verticesEccentricities))
            self.periphery = list(filter(max, verticesEccentricities))
        else:
            self.radius = float('inf')
            self.diameter = float('inf')
            self.verticesEccentricities = {vertex.getLabel():float('inf') for vertex in self}
            self.center = list()
            self.periphery = list()

    def addVertex(self, vertex) -> None:
        if vertex.getLabel() not in self.verticesSet:
            self.verticesSet[vertex.getLabel()] = vertex
            self.verticesDegrees[vertex.getLabel()] = vertex.getDegree()
        else:
            raise ValueError("Duplicate vertex")
        self._dirty = True
    
    def addEdge(self, edge) -> None:
        endPoints = list(edge.getEndPoints())
        for vertex in endPoints:
            if vertex.getLabel() not in self.verticesSet:
                raise ValueError("Vertex not in graph")
        endPoints[0].addAdjacent(endPoints[1])
        endPoints[1].addIncidentEdge(edge)
        if not self.isDigraph:
            endPoints[1].addAdjacent(endPoints[0])
            endPoints[0].addIncidentEdge(edge)
        self.edgesSet.add(edge)
        self._dirty = True
    
    def getVertices(self) -> dict:
        return self.verticesSet
    
    def getVertex(self, label: str):
        if label in self:
            return self.verticesSet[label]
        raise NameError(label)
    
    def getEdges(self) -> set:
        return self.edgesSet

    def getOrder(self) -> int:
        return len(self)
    
    def getSize(self) -> int:
        return len(self.edgesSet)

    def getDegree(self) -> int:
        # by theorem
        return 2 * len(self.edgesSet)
    
    def getMinDegree(self) -> int:
        return min(self.verticesDegrees.values())
    
    def getMaxDegree(self) -> int:
        return max(self.verticesDegrees.values())
    
    def isNull(self) -> bool:
        return len(self.verticesSet) == 0 and len(self.edgesSet) == 0

    # def isSubgraphOf(self, other) -> bool:
    #     isSubgraph = True
    #     for v in self:
    #         isSubgraph &= v in other
    #     isSubgraph &= self.edgesSet <= other.edgesSet
    #     return isSubgraph
    
    def getEccentricityOf(self, vertex) -> int:
        # max d(u,v)
        pass

    def getRadius(self) -> int:
        # min eccentricity
        if self._dirty:
            self.update()
            self._dirty = False
        return self.radius

    def getDiameter(self) -> int:
        # max eccentricity
        if self._dirty:
            self.update()
            self._dirty = False
        return self.diameter
    
    def getPeriphery(self):
        # set o peripheral points
        if self._dirty:
            self.update()
            self._dirty = False
        return self.periphery
    
    def getCenter(self):
        # set of central points
        if self._dirty:
            self.update()
            self._dirty = False
        return self.center