from typing import Iterator

class Vertex:
    def __init__(self, label: str):
        self.__label: str = label
        # self.__eccentricity = None #se asume el vertice aislado
        self.__adjacents: set = set()
        self.__incidentEdges: set = set()
    
    def __str__(self):
        return f'{self.__label}'
    
    def __iter__(self):
        return iter(self.__adjacents)

    def getLabel(self) -> str:
        return self.__label
    
    def getDegree(self) -> int:
        return len(self.__incidentEdges)
    
    # def getEccentricity(self) -> float:
    #     return self.__eccentricity if self.__eccentricity != None else float('inf')

    def getAdjacents(self) -> set:
        return self.__adjacents
    
    def isAdjacentOf(self, other) -> bool:
        return other in self.__adjacents
    
    def getAdjacentsCount(self) -> int:
        return len(self.__adjacents)
    
    def isIsolated(self) -> bool:
        return len(self.__adjacents) == 0 and len(self.__incidentEdges) == 0

    def addAdjacent(self, other) -> None:
        self.__adjacents.add(other)
    
    def addIncidentEdge(self, edge) -> None:
        self.__incidentEdges.add(edge)

class Edge:
    def __init__(self, v1, v2):
        self.__endPoints = set([v1, v2])

    def __iter__(self):
        return iter(self.__endPoints)
    
    def __str__(self):
        return f'{self.__endPoints[0]}<--->{self.__endPoints[1]}'

    def getEndPoints(self) -> set:
        return self.__endPoints
    
    def isLoop(self) -> bool:
        return self.__endPoints[0] == self.__endPoints[1]
        
class Graph:
    def __init__(self, verticesSet: dict = None, edgesSet: set = None):
        self.__verticesSet: dict = verticesSet or {}
        self.__edgesSet: set = edgesSet or set()
    
    def __iter__(self) -> Iterator:
        return iter(self.__verticesSet)
    
    def __contains__(self, vertex) -> bool:
        return vertex in self.__verticesSet
    
    def __len__(self) -> int:
        return len(self.__verticesSet)
    
    def __add__(self, other):
        return Graph({**self.__verticesSet, **other.verticesSet}, self.__edgesSet+other.edgesSet)
        #Py3.9#return Graph(self.__verticesSet | other.verticesSet, self.__edgesSet+other.edgesSet)

    def isConnected(self) -> bool:
        if len(self.__verticesSet) == 0:
            return True
        visited = set()
        q = []
        origin = self.__verticesSet.values()[0]
        visited.add(origin)
        q.append(origin)
        while len(q) != 0:
            vertex = q.pop(0)
            for adjacent in vertex.getAdjacents():
                if not adjacent in visited:
                    visited.add(adjacent)
                    q.append(adjacent)
        return self.__verticesSet == visited

    def addVertex(self, vertex) -> None:
        if vertex.getLabel() not in self.__verticesSet:
            self.__verticesSet[vertex.getLabel()] = vertex
            self.__verticesDegrees[vertex.getLabel()] = vertex.getDegree()
        else:
            raise ValueError("Duplicate vertex")
    
    def addEdge(self, edge) -> None:
        endPoints = list(edge.getEndPoints())
        for vertex in endPoints:
            if vertex.getLabel() not in self.__verticesSet:
                raise ValueError("Vertex not in graph")
        endPoints[0].addAdjacent(endPoints[1])
        endPoints[1].addIncidentEdge(edge)
        if not self.__isDigraph:
            endPoints[1].addAdjacent(endPoints[0])
            endPoints[0].addIncidentEdge(edge)
        self.__edgesSet.add(edge)
    
    def removeVertex(self) -> Vertex:
        pass

    def removeEdge(self) -> Edge:
        pass

    def getVertices(self) -> dict:
        return self.__verticesSet
    
    def getVertex(self, label: str) -> Vertex:
        if label in self:
            return self.__verticesSet[label]
        raise NameError(label)

    def getEdge(self) -> Edge:
        pass
    
    def getEdges(self) -> set:
        return self.__edgesSet

    def getOrder(self) -> int:
        return len(self)
    
    def getSize(self) -> int:
        return len(self.__edgesSet)

    def getDegree(self) -> int:
        # by theorem
        return 2 * len(self.__edgesSet)
    
    def getMinDegree(self) -> int:
        return min(self.__verticesDegrees.values())
    
    def getMaxDegree(self) -> int:
        return max(self.__verticesDegrees.values())