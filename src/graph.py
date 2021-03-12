from typing import Iterator, Any

class Graph:
	def __init__(self, is_directed: bool = False, vertices_init: list = []) -> None:
		self.__vertices = {}
		for v in vertices_init:
			self.__vertices[v] = {}
		self.__is_directed = is_directed

	def __contains__(self, v: str) -> bool:
		return v in self.__vertices

	def __len__(self) -> int:
		return len(self.__vertices)

	def __iter__(self) -> Iterator:
		return iter(self.__vertices)

	def add_vertex(self, v: str) -> None:
		if v in self:
			raise ValueError(f"Ya hay un vertice {str(v)} en el grafo")
		self.__vertices[v] = {}

	def __validate_vertex(self, v: str) -> None:
		if v not in self:
			raise ValueError(f"No hay un vertice {str(v)} en el grafo")

	def __validate_vertices(self, v: str, w: str) -> None:
		self.__validate_vertex(v)
		self.__validate_vertex(w)

	def borrar_vertice(self, v: str) -> None:
		self.__validate_vertex(v)
		for w in self:
			if v in self.__vertices[w]:
				del self.__vertices[w][v]
		del self.__vertices[v]

	def add_edge(self, v: str, w: str, peso: Any = None) -> None:
		self.__validate_vertices(v, w)
		if self.are_joined(v, w):
			raise ValueError("El vertice " + str(v) + " ya tiene como adyacente al vertice " + str(w))
		
		self.__vertices[v][w] = peso
		if not self.__is_directed:
			self.__vertices[w][v] = peso

	def remove_edge(self, v: str, w: str) -> None:
		self.__validate_vertices(v, w)
		if not self.are_joined(v, w):
			raise ValueError("El vertice " + str(v) + " no tiene como adyacente al vertice " + str(w))

		del self.__vertices[v][w]
		if not self.__is_directed:
			del self.__vertices[w][v]

	def are_joined(self, v: str, w: str) -> bool:
		return w in self.__vertices[v]

	def edge_weight(self, v: str, w: str) -> Any:
		if not self.are_joined(v, w):
			raise ValueError("El vertice " + str(v) + " no tiene como adyacente al vertice " + str(w))
		return self.__vertices[v][w]

	def get_vertices(self) -> list:
		return list(self.__vertices.keys())

	def random_vertex(self) -> str:
		return self.get_vertices()[0]

	def adjacents(self, v: str) -> list:
		self.__validate_vertex(v)
		return list(self.__vertices[v].keys())
	
	def order(self) -> int:
		return len(self)

	def __str__(self) -> str:
		cad = ""
		for v in self:
			cad += v
			for w in self.adjacents(v):
				cad += " -> " + w 
			cad += "\n"
		return cad