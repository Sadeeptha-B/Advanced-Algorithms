class Graph:
    def __init__(self) -> None:
        pass


class Vertex:
    def __init__(self, key) -> None:
        self.key = key
        self.edges = []
        self.discovered = False

    def __str__(self):
        return str(self.key)
     

class Edge:
     def __init__(self,u, v, w=None) -> None:
          self.u = u
          self.v = v
          self.w = w
    

if __name__ == "__main__":
        pass