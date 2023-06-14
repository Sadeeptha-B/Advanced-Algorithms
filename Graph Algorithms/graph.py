'''
Author: Sadeeptha Bandara
'''
from typing import List, Tuple, Optional,  Any
import heapq

# Custom types
Key = int
Prop = Any
Weight = float 
Distance = Weight
Vertex_Input = List[Prop]
Edge_Input = List[Tuple[Key, Key]] | List[Tuple[Key, Key, Weight]] 


'''
Graph class with bfs, dfs, shortest distance implementations
'''
class Graph:
    # Adjacency list representation
    # O(E)
    def __init__(self, vertices: Vertex_Input, edge_tuples: Edge_Input) -> None:

        # If supporting non-int keys will need to modify
        self.vertices: List[Optional[Vertex]] = [None] * (len(vertices) + 1)
        
        # Set vertices
        for ind, prop in enumerate(vertices):
            key = ind + 1
            self.vertices[key]  = Vertex(key, prop)

        # Set edges
        for elem in edge_tuples:
            u = self.find_vertex(elem[0])
            v = self.find_vertex(elem[1])

            w = 1 if len(elem) == 2 else elem[2]

            u.add_edge(Edge(u, v, w))
            v.add_edge(Edge(v, u, w))

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
    o(v* heap serve + e * heap update)
    Requires to maintain priority queue to find shortest path
    Adding types made this seem more complicated than it is


    Returns three return values
    1.Shortest distance to sink from source
    2. The shortest path from source to sink backwards
    3. The distances thus far finalized till sink is reached

    If sink is not reached,
    1. Infinity
    2. Empty since no path exists
    3. Distances computed from source
    '''
    def dijsktra(self, src_key:Key, sink_key:Key):
        discovered: List[Tuple(Distance, Key)] = []   # Priority queue to serve nearest vertex
        distances:List[Tuple(Key,Prop, Distance)] = []  # Distances of finalized vertices

        # Init
        src = self.find_vertex(src_key)
        src.distance = 0
        src.discovered = True
        heapq.heappush(discovered, (src.distance, src.get_key()))

        # Go over each connected vertex
        while len(discovered) > 0:
            u_key = heapq.heappop(discovered)[1]
            u = self.find_vertex(u_key)
            u.visited = True
            distances.append((u.get_key(), u.get_property(),  u.distance))

            # Terminate if sink reached
            if u_key == sink_key:
                res = self.__backtrack(u)
                dist = u.distance
                self.reset()
                return dist, res, distances

            # Edge relaxation
            for edge in u.get_edges():
                v = edge.v

                # Discover vertex for the first time
                if not v.discovered:
                    v.discovered = True
                    v.distance = u.distance + edge.w
                    v.previous = u
                    heapq.heappush(discovered, (v.distance, v.get_key()))
                    continue
                
                # Update distance if shorter path found
                if not v.visited:
                    new_dist = u.distance + edge.w
                    if v.distance > new_dist:
                        # Update value on heap
                        ind = discovered.index((v.distance, v.get_key()))     
                        discovered.pop(ind)   #Potentially O(n), but can be O(logn) if implemented efficiently
                        heapq.heappush(discovered, (new_dist, v.get_key()))

                        v.distance = new_dist
                        v.previous = u

        self.reset()

        # Destination is not reachable
        return float('inf'), [], distances
    

    def __backtrack(self, curr:'Vertex') -> List[Tuple[Key, Prop]]:
        res = []
        while curr.previous is not None:
            previous = curr.previous
            key = previous.get_key()
            prop = previous.get_property()
            res.append((key, prop))
            curr = previous
            
        return res


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
        self.distance:Weight = 0
        self.previous: Optional[Vertex] = None

    def __str__(self) -> str:
        return str(self.__key)
     
    def add_edge(self, edge: 'Edge'):
        self.__edges.append(edge)

    def reset(self)-> None:
        self.discovered = False
        self.visited = False
        self.distance = 0
        self.previous = None

    def get_edges(self) -> List['Edge']:
        return list(self.__edges)
    
    def get_property(self) -> Prop:
        return self.__prop
    
    def get_key(self) -> Key:
        return Key(self.__key)
    

class Edge:
     def __init__(self,u:Vertex, v:Vertex, w: float=1) -> None:
          self.u = u
          self.v = v
          self.w = w
    



if __name__ == "__main__":
    
    # Provide the vertex property value, keys will be added by the graph implementation
    # Vertex keys will be in the provided order 1....n 
    test_vertices:List[Vertex_Input] = [[1,2,3,4,5,6],  [2, 7, 5, 2, 10, 6, 9, 5, 11, 4], [2,1,3, 0, 4]] 
    
    # Undirected_edges
    # Edges must be according to key values of vertices, this is because properties (vertex value) can be non unique
    test_edges:List[Edge_Input]= [[(1,5), (1,2), (2,5), (2,3), (3,4), (4,5), (4,6)], [(1,2), (1,3), (2,4), (2,5), (2, 6), (3,7), (6, 8), (6, 9), (7, 10)],  [(1,2,1), (1,3,2), (2,4,3), (2,3,4), (3,4,7), (3,5,3),(4,5, 8)]]
   
    graph = Graph(test_vertices[2], test_edges[2])
    print(graph.bfs(1))
    print(graph.dfs(1))
    print(graph.dijsktra(1,5))
