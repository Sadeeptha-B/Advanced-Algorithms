'''
Author: Sadeeptha Bandara
'''
from typing import List, Tuple, Optional,  Any


# Custom types
Key = int
Prop = Any
Vertices = List[Prop]
Edges = List[Tuple[Key, Key]]


'''
Graph class with bfs, dfs, shortest distance implementations
'''
class Graph:
    # Adjacency list representation
    # O(E)
    def __init__(self, vertices: Vertices, edge_tuples: Edges) -> None:

        # If supporting non-int keys will need to modify
        self.vertices: List[Optional[Vertex]] = [None] * (len(vertices) + 1)
        
        # Set vertices
        for ind, prop in enumerate(vertices):
            key = ind + 1
            self.vertices[key]  = Vertex(key, prop)

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

            u = discovered.pop(0) # Linked list implmt O(1)/ 
            # or could've used pointers with termination condition

        self.reset()
        return res

    '''
    Reset vertex marking 
    '''
    def reset(self)-> None:
        for vertex in self.vertices:
            if vertex is None:
                continue

            vertex.reset()


    '''
    Depth first search
    Provide key of starting node
    '''
    def dfs(self, k: Key)-> List[Prop]:
        res = []
        u = self.find_vertex(k)

        self.__dfs_aux(u, res)
        self.reset()
        return res
        

    def __dfs_aux(self, u:'Vertex', res:List[Prop])-> None:
        res.append(u.get_property())
        u.visited = True

        for edge in u.get_edges():
            v = edge.v
            if not v.visited:
                self.__dfs_aux(v, res)


    '''
    Dijsktra's algorithm to find the shortest path to any vertex
    O(vlogv + elogv) --> O(elogv) dominant factor
    Requires to maintain priority queue to find shortest path
    '''
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
        self.distance:float = 0

    def __str__(self) -> str:
        return str(self.__key)
     
    def add_edge(self, edge: 'Edge'):
        self.__edges.append(edge)

    def reset(self)-> None:
        self.discovered = False
        self.visited = False
        self.distance = 0

    def get_edges(self) -> List['Edge']:
        return list(self.__edges)
    
    def get_property(self) -> Prop:
        return self.__prop
    

class Edge:
     def __init__(self,u:Vertex, v:Vertex, w: Optional[float]=None) -> None:
          self.u = u
          self.v = v
          self.w = w
    



if __name__ == "__main__":
    
    # Provide the vertex property value, keys will be added by the graph implementation
    # Vertex keys will be in the provided order 1....n 
    test_vertices:List[Vertices] = [[1,2,3,4,5,6],  [2, 7, 5, 2, 10, 6, 9, 5, 11, 4]]
    
    # Undirected_edges
    # Edges must be according to key values of vertices, this is because properties (vertex value) can be non unique
    test_edges:List[Edges]= [[(1,5), (1,2), (2,5), (2,3), (3,4), (4,5), (4,6)], [(1,2), (1,3), (2,4), (2,5), (2, 6), (3,7), (6, 8), (6, 9), (7, 10)]]
   
    graph = Graph(test_vertices[0], test_edges[0])
    print(graph.bfs(1))
    print(graph.dfs(1))
