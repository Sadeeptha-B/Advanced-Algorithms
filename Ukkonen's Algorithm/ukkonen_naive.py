ALPHABET_SIZE = 91
ASCII_START = 36

def ukkonen_naive(st):
    st = st + "$"
    n = len(st)
    root = Node()

    # Loop over phases
    for i in range(n):
        j = 0

        # Loop over extensions
        while j <= i:
            char = st[j]
            ind = ord(char) - ASCII_START
            edge = root.edges[ind]
            suffix = st[j:i+1]

            if edge is None:
                root.edges[ind] = Edge(suffix)
                j += 1
                continue

            # Loop while within bounds

            # If difference within bounds
                # create node
            # If no difference
                # rule 3: do nothing
            
            # If outside bounds
                # If another edge is present
                    # Go to said edge
                # No edge present: do leaf extension

            for ind, char in enumerate(edge.suffix):
                # Rule 2 in the middle
                if char != suffix[ind]:
                    node = Node()
                    node.edges[ord(char) - ASCII_START] = Edge(edge.suffix[ind:i+1])
                    node.edges[ord(suffix[ind]) - ASCII_START] = Edge(suffix[ind:i+1])
                    edge.suffix = edge.suffix[0:ind]

                    edge_node = node.edges[ord(char) - ASCII_START]
                    edge_node.next = edge.next
                    edge.next = node

            
            j+=1


class Node:
    def __init__(self):
        self.edges = [None] * ALPHABET_SIZE

class Edge:
    def __init__(self, suffix):
        self.suffix = suffix
        self.next = None



if __name__ == "__main__":
    ukkonen_naive("apple")