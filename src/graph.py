from typing import Any, Iterator

class Vertex:
    def __init__(self, label: str, data: Any = None, color: str = "black"):
        self.__label: str = label
        self.__color: str = color
        self.__data: Any = data
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
    
    def getColor(self) -> str:
        return self.__color
    
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
    def __init__(self, v1: Vertex, v2: Vertex, w: Any = None):
        self.__endPoints = [v1, v2]
        self.__weight = w

    def __iter__(self):
        return iter(self.__endPoints)

    def getEndPoints(self) -> list:
        return self.__endPoints
    
    def isLoop(self) -> bool:
        return self.__endPoints[0] == self.__endPoints[1]
    
    def getWeight(self) -> any:
        return self.__weight
        
class Graph:
    def __init__(self, verticesSet: dict = None, edgesSet: set = None):
        self.__verticesSet: dict = verticesSet or {}
        self.__edgesSet: set = edgesSet or {}
    
    def __iter__(self) -> Iterator:
        return iter(self.__verticesSet)
    
    def __contains__(self, vertex: str) -> bool:
        return vertex in self.__verticesSet
    
    def __len__(self) -> int:
        return len(self.__verticesSet)
    
    def __add__(self, other):
        return Graph({**self.__verticesSet, **other.verticesSet}, self.__edgesSet+other.edgesSet)
        #Py3.9#return Graph(self.__verticesSet | other.verticesSet, self.__edgesSet+other.edgesSet)
    
    def __str__(self):
        out_str = ""
        # for e in self.__edgesSet:
        #     out_str += str(e.getEndPoints())
        #     out_str += '\n'
        for v in self.__verticesSet.values():
            out_str += v.getLabel()
            for w in v.getAdjacents():
                out_str += " <---> " + w.getLabel()
            out_str += "\n"
        return out_str

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

    def addVertex(self, vertex: Vertex) -> None:
        label = vertex.getLabel()
        if label not in self.__verticesSet:
            self.__verticesSet[label] = vertex
            # self.__verticesDegrees[vertex.getLabel()] = vertex.getDegree()
        # else:
        #     raise ValueError("Duplicate vertex")
    
    def addEdge(self, edge: Edge) -> None:
        endPoints = edge.getEndPoints()
        for vertex in endPoints:
            if vertex.getLabel() not in self.__verticesSet:
                raise ValueError("Vertex not in graph")
        endPoints[0].addAdjacent(endPoints[1])
        endPoints[1].addIncidentEdge(edge)
        endPoints[1].addAdjacent(endPoints[0])
        endPoints[0].addIncidentEdge(edge)
        self.__edgesSet[endPoints[0].getLabel()+endPoints[1].getLabel()] = edge
    
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

    def getEdge(self, vertex_a: Vertex, vertex_b: Vertex) -> Edge:
        a = vertex_a.getLabel()
        b = vertex_b.getLabel()
        return self.__edgesSet[a+b] if a+b in self.__edgesSet else self.__edgesSet[b+a]
    
    def getEdges(self) -> set:
        return self.__edgesSet

    def getOrder(self) -> int:
        return len(self)

    def getOrderOf(self, color: str) -> int:
        order = 0
        for v in self.__verticesSet:
            if self.__verticesSet[v].getColor() == color:
                order += 1
        return order
    
    def getSize(self) -> int:
        return len(self.__edgesSet)

    def getDegree(self) -> int:
        # by theorem
        return 2 * len(self.__edgesSet)
    
    def getMinDegree(self) -> int:
        return min(self.__verticesDegrees.values())
    
    def getMaxDegree(self) -> int:
        return max(self.__verticesDegrees.values())