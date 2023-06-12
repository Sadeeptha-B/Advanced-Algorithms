'''
Author: Sadeeptha Bandara
'''
from typing import List, Tuple, Optional, Type


# Custom types
Key = int
Vertices = List[Key]
Edges = List[Tuple[Key, Key]]


'''
Graph class with bfs, dfs, shortest distance implementations
'''
class Graph:
    # Adjacency list representation
    def __init__(self, vertex_keys: Vertices, edge_tuples: Edges) -> None:

        # If supporting non-int keys will need to modify, or if dealing with a lot
        # of vertices
        self.vertices: List[Optional[Vertex]] = [None] * (max(vertex_keys)+1)
        for key in vertex_keys:
            self.vertices[key] = Vertex(key)

        for u_key, v_key in edge_tuples:
            u = self.find_vertex(u_key)
            v = self.find_vertex(v_key)

            u.add_edge(Edge(u, v))
            v.add_edge(Edge(v, u))


    def find_vertex(self, key:Key) -> 'Vertex':
        try:
            vertex = self.vertices[key]
        except IndexError:
            raise KeyError(f'Vertex {key} does not exist')
        else:
            return vertex
        


'''
Vertex key must be unique
'''
class Vertex:
    def __init__(self, key:Key) -> None:
        self.key = key
        self.edges: List[Edge] = []
        self.discovered:bool = False

    def __str__(self) -> str:
        return str(self.key)
     
    def add_edge(self, edge: 'Edge'):
        self.edges.append(edge)
        


class Edge:
     def __init__(self,u:Vertex, v:Vertex, w: Optional[int]=None) -> None:
          self.u = u
          self.v = v
          self.w = w
    


if __name__ == "__main__":
    vertex_values:Vertices = [1,2,3,4,5,6]

    #Undirected
    edge_tuples:Edges = [(1,5), (1,2), (2,5), (2,3), (3,4), (4,5), (4,6)]

    graph = Graph(vertex_values, edge_tuples)

