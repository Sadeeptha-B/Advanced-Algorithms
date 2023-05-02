ALPHABET_SIZE = 91
ASCII_START = 36


'''
Ukkonen's algorithm builds a suffix tree in phases
At each phase, it will perform the necessary extensions to create
the implicit suffix tree for [1..i]

In doing so, it will have to perform the extensions for each suffix of the 
implicit suffix tree [1..i]
To do the extensions for each of these it will need to traverse to the necessary spot in 
the tree.

'''
class Ukkonen:
    def __init__(self, st):
        self.st = st
        self.root = Node()
        self.__global_end = End()

        # Link root to itself
        self.root.link = self.root
        self.run()


    def run(self):
        st = self.st + "$"
        n = len(st)

        # Initialize extension index, active node
        j = 0 
        active_node = self.root

        # Loop over phases
        for i in range(n):
            # Trick 1: Global end 
            self.__global_end.increment()

            if j == i:
                ind = ord(st[j]) - ASCII_START
                edge = active_node.edges[ind]

                # Rule 2 alternate
                if edge is None:
                    # Trick 2: start, end representation
                    active_node.edges[ind] = Edge(j, self.__global_end)
                    j += 1
                else:
                    active_edge = edge
                    active_ptr = 0

                continue

            while j < i:
                active_edge = active_node.edges[ord(st[i]) - ASCII_START]

                # Trick 3: Skip count traversal
                suffix_len = i - j + 1

                while suffix_len > len(active_edge):
                    # Next node: this MUST be present
                    active_node = active_edge.next

                    # Subtract edge traversal
                    suffix_len -= len(active_edge)

                    # next suffix char
                    suffix_char =  st[j + len(active_edge)]

                    # next active_edge: this edge MUST be present because rule 1 extensions should already be covered
                    active_edge = active_node.edges[ord(suffix_char) - ASCII_START]


                # After skip count traversal: case 2 or case 3 must occur    
                # Comparing the suffix extension char and the edge character
                comp_ind = active_edge.start + active_ptr + 1
                edge_char = st[comp_ind]       
                extension = st[i]

                # Rule 3
                if extension == edge_char:
                    active_ptr += 1
                    break
                # Rule 2
                else:
                    node = Node()    
                    node.edges[ord(extension) - ASCII_START] = Edge(i, self.__global_end)
                    node.edges[ord(edge_char) - ASCII_START] = Edge(comp_ind, self.__global_end)
                    node.link = self.root
                    active_edge.end = End(comp_ind - 1)
                    active_edge.next = node

                    

                active_node = active_node.link
                j += 1


        

    def generate_suffix_array(self):
        arr = []
        return arr






'''
Class to keep track of global end since Python does not pass values by reference
'''
class End:
    def __init_(self, val=-1):
        self.value = val

    def increment(self, val=1):
        self.value += val


# Suffix tree components
# ===============================================================================================

class Node:
    def __init__(self, link=None):
        self.edges = [None]*ALPHABET_SIZE
        self.link = None


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end= end
        self.next = None

    def __len__(self):
        return self.end.value - self.start + 1


if __name__ == "__main__":
    ukkonen = Ukkonen("abcabxabcyab")
    suffix_array = ukkonen.generate_suffix_array()
    print(suffix_array)

