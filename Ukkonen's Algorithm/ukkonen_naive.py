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
                root.edges[ind] = Edge(suffix, j)
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
                        node.edges[ord(char) - ASCII_START] = Edge(suffix[ind:i+1], j)
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
                    node.edges[ord(char) - ASCII_START] = Edge(suffix[ind:i+1], j)
                    node.edges[ord(edge.suffix[edge_ind]) - ASCII_START] = Edge(edge.suffix[edge_ind:i+1], edge.suffix_id)

                    edge_node = node.edges[ord(edge.suffix[edge_ind]) - ASCII_START]
                    edge_node.next = edge.next
                    edge.next = node
                    edge.suffix = edge.suffix[0:edge_ind]
                    edge.suffix_id = None
                    break

                if ind + 1 == len(suffix):
                    print(suffix, j, i , "rule3")

                edge_ind += 1

            j+=1

    return root


def generate_suffix_array(root):
    arr = []
    inorder_aux(root, arr)
    return arr

def inorder_aux(node, arr):
    for edge in node.edges:
        if edge is None:
            continue

        if edge.next is None:
            arr.append(edge.suffix_id)
        else:
            inorder_aux(edge.next, arr)



class Node:
    def __init__(self):
        self.edges = [None] * ALPHABET_SIZE

class Edge:
    def __init__(self, suffix, suffix_id=None):
        self.suffix = suffix
        self.next = None
        self.suffix_id = suffix_id

    def __len__(self):
        return len(self.suffix)
    
    def add_char(self, char):
        self.suffix += char



if __name__ == "__main__":
    # ukkonen_naive("apple")
    root = ukkonen_naive("abcabxazabyabcyab")
    print(generate_suffix_array(root))
