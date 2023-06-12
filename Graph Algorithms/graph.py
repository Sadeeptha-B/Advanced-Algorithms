'''
Author: Sadeeptha Bandara
'''
from typing import List, Tuple, Optional,  Any


# Custom types
Key = int
Prop = Any
Vertices = List[Tuple[Key, Prop]]
Edges = List[Tuple[Key, Key]]


'''
Graph class with bfs, dfs, shortest distance implementations
'''
class Graph:
    # Adjacency list representation
    # O(E)
    def __init__(self, vertex_keys: Vertices, edge_tuples: Edges) -> None:

        # If supporting non-int keys will need to modify

        max_key = max(vertex_keys, key=lambda elem:elem[0])[0]
        self.vertices: List[Optional[Vertex]] = [None] * (max_key+1)
        
        # Set vertices
        for key, prop in vertex_keys:
            self.vertices[key] = Vertex(key, prop)


        # Set edges
        for u_key, v_key in edge_tuples:
            u = self.find_vertex(u_key)
            v = self.find_vertex(v_key)

            u.add_edge(Edge(u, v))
            v.add_edge(Edge(v, u))

    '''
    Convenience function to find a vertex. Abstracted to allow easy modification
    for alternative self.vertices implementation
    '''
    def find_vertex(self, key:Key) -> 'Vertex':
        try:
            vertex = self.vertices[key]
        except IndexError:
            raise KeyError(f'Vertex {key} does not exist')
        else:
            return vertex
        
    # O(V+E)
    '''
    Breadth first search
    Provide key of starting node
    '''
    def bfs(self, key:Key)-> List[Prop]:
        discovered = []
        res = []

        u = self.find_vertex(key)
        discovered.append(u)
        res.append(u.get_property())
        u.discovered = True

        while len(discovered) > 0:
            for edge in u.get_edges():
                v = edge.v
                if not v.discovered:
                    discovered.append(v)
                    res.append(v.get_property())
                    v.discovered = True

            u = discovered.pop(0) # Linked list implmt O(1)

        self.reset()
        return res

    '''
    Reset vertex marking 
    '''
    def reset(self):
        for vertex in self.vertices:
            if vertex is None:
                continue

            vertex.reset()


    '''
    Depth first search
    Provide key of starting node
    '''
    def dfs(self, k: Key)-> List[Key]:
        res = []
        u = self.find_vertex(k)

        self.__dfs_aux(u, res)
        self.reset()
        return res
        

    def __dfs_aux(self, u:'Vertex', res:List[Key])-> None:
        res.append(u.get_property())
        u.visited = True

        for edge in u.get_edges():
            v = edge.v
            if not v.visited:
                self.__dfs_aux(v, res)


    def dijsktra(self, k:Key)-> List[Key]:
        pass


'''
Vertex key must be unique
'''
class Vertex:
    def __init__(self, key:Key, prop: Prop) -> None:
        self.__key = key
        self.__prop = prop
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
    
    def get_property(self) -> Prop:
        return self.__prop
    

class Edge:
     def __init__(self,u:Vertex, v:Vertex, w: Optional[int]=None) -> None:
          self.u = u
          self.v = v
          self.w = w
    



if __name__ == "__main__":
    
    # Undirected_edges
    test_vertices:List[Vertices] = [[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6)],  [(1,2), (2,7), (3,5), (4, 2), (5,10), (6, 6), (7, 9), (8, 5), (9, 11), (10, 4)]]
    test_edges:List[Edges]= [[(1,5), (1,2), (2,5), (2,3), (3,4), (4,5), (4,6)], [(1,2), (1,3), (2,4), (2,5), (2, 6), (3,7), (6, 8), (6, 9), (7, 10)]]
   
    graph = Graph(test_vertices[1], test_edges[1])
    print(graph.bfs(1))
    print(graph.dfs(1))

