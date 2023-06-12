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
    # O(E)
    def __init__(self, vertex_keys: Vertices, edge_tuples: Edges) -> None:

        # If supporting non-int keys will need to modify, or if dealing with a lot
        # of vertices
        self.vertices: List[Optional[Vertex]] = [None] * (max(vertex_keys)+1)
        
        # Set vertices
        for key in vertex_keys:
            self.vertices[key] = Vertex(key)


        # Set edges
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
        
    # O(V+E)
    def bfs(self, key:Key)-> List[Key]:
        discovered = []
        res = []

        u = self.find_vertex(key)
        discovered.append(u)
        res.append(u.get_key())
        u.discovered = True

        while len(discovered) > 0:
            for edge in u.get_edges():
                v = edge.v
                if not v.discovered:
                    discovered.append(v)
                    res.append(v.get_key())
                    v.discovered = True

            u = discovered.pop(0) # Linked list implmt O(1)

        self.reset()
        return res


    def reset(self):
        for vertex in self.vertices:
            if vertex is None:
                continue

            vertex.reset()


    def dfs(self, k: Key)-> List[Key]:
        res = []
        u = self.find_vertex(k)

        self.__dfs_aux(u, res)
        self.reset()
        return res
        

    def __dfs_aux(self, u:'Vertex', res:List[Key])-> None:
        res.append(u.get_key())
        u.visited = True

        for edge in u.get_edges():
            v = edge.v
            if not v.visited:
                self.__dfs_aux(v, res)



'''
Vertex key must be unique
'''
class Vertex:
    def __init__(self, key:Key) -> None:
        self.__key = key
        self.__edges: List[Edge] = []
        self.discovered:bool = False
        self.visited:bool = False

    def __str__(self) -> str:
        return str(self.__key)
     
    def add_edge(self, edge: 'Edge'):
        self.__edges.append(edge)

    def reset(self)-> None:
        self.discovered = False
        self.visited = False

    def get_edges(self) -> List['Edge']:
        return list(self.__edges)
    
    def get_key(self)-> Key:
        return Key(self.__key)
    

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
    print(graph.bfs(1))
    print(graph.dfs(1))

