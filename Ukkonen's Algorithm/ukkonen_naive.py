ALPHABET_SIZE = 91
ASCII_START = 36


'''
Fully Naive Ukkonen's algorithm
- Builds implicit suffix tree for each phase O(N)
- Within a phase, considers each suffix O(N)
- For each such extension, traverses to the end of the suffix and performs relevant extension O(N)
    - Leaf extension
    - leaf from internal node (existing or new)
    - do nothing
- Although string slicing is used in these rules, the total aggregate traversal complexity sums up to O(N)
- Therefore, total complexity O(N^3)
'''
def ukkonen_naive(st):
    st = st + "$"
    n = len(st)
    root = Node()

    # Loop over phases
    for i in range(n):
        print("========")   
        j = 0

        # Loop over extensions
        while j <= i:
            ind = ord(st[j]) - ASCII_START
            edge = root.edges[ind]
            suffix = st[j:i+1]

            if edge is None:
                root.edges[ind] = Edge(suffix)
                print(suffix, j, i, "rule2:alt")
                j += 1
                continue

            edge_ind = 0

            # Traversal of suffix within extension
            for ind, char in enumerate(suffix):

                # End of edge
                if edge_ind == len(edge):
                    # Case 1
                    if edge.next is None:
                        print(suffix, j, i, "rule1")
                        edge.add_char(char)
                        break

                    node = edge.next
                    current = node.edges[ord(char) - ASCII_START]

                    # Rule 2: alternate
                    if current is None:
                        node.edges[ord(char) - ASCII_START] = Edge(suffix[ind:i+1])
                        print(suffix, j, i, "rule2:alt")
                        break
                    else:
                        edge = current
                        edge_ind = 0


                # Rule 2: General 
                # The inequal case should be at last ind
                if char != edge.suffix[edge_ind]:
                    print(suffix, j, i, "rule2:general")
                    node = Node()
                    node.edges[ord(char) - ASCII_START] = Edge(suffix[ind:i+1])
                    node.edges[ord(edge.suffix[edge_ind]) - ASCII_START] = Edge(edge.suffix[edge_ind:i+1])

                    edge_node = node.edges[ord(edge.suffix[edge_ind]) - ASCII_START]
                    edge_node.next = edge.next
                    edge.next = node
                    edge.suffix = edge.suffix[0:edge_ind]
                    break

                if ind + 1 == len(suffix):
                    print(suffix, j, i , "rule3")

                edge_ind += 1

            j+=1


class Node:
    def __init__(self):
        self.edges = [None] * ALPHABET_SIZE

class Edge:
    def __init__(self, suffix):
        self.suffix = suffix
        self.next = None

    def __len__(self):
        return len(self.suffix)
    
    def add_char(self, char):
        self.suffix += char



if __name__ == "__main__":
    # ukkonen_naive("apple")
    ukkonen_naive("abcabxabcyab")