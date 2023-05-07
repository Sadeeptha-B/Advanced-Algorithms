'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = "output_sa.txt"
ALPHABET_SIZE = 91  # 126 - 37 + 2
ASCII_START = 36    #Starting ASCII char
TERMINAL_CHAR = "$"


'''
Class to modularize ukkonen components
'''
class Ukkonen:
    def __init__(self, st):
        self.st = st
        self.root = Node()
        self.root.link = self.root

        self.__global_end = End()
        self.run()


    '''
    Builds suffix tree in phases. In each phase i, constructs the implicit 
    suffix tree for [0..i] (0 based indexing). Maintains the following variables

    i - The current phase
    j - The starting index of the suffix within a phase that is being extended
    active_node - The current node during tree traversal
    active_edge - The current edge during traversal (this is connected to the active_node)
    curr_ind - Index within [j..i] that corresponds to the tree position of active_edge.start
                (Useful when skip counting)
    remaining - The remaining length of the suffix after traversal: len([curr_ind.. i])
    '''
    def run(self):
        st = self.st + TERMINAL_CHAR
        n = len(st)

        # Initialisation
        i, j = 0, 0 
        active_node = self.root
        active_edge = None
        curr_ind = j
        previous= None

        # Loop over phases
        while i < n:

            # Maintain global end
            self.__global_end.set_value(i)
            edge = active_node.get_edge(st[curr_ind])

            # Handle all rule 2 alternate cases
            if edge is None:
                active_node.set_edge(st[curr_ind], Edge(curr_ind, self.__global_end, j))
                
                # Suffix link manipulation
                if previous is not None:
                    previous.link = active_node
                    previous = None
                active_node = active_node.link

                # Move to next phase
                if i == j:
                    previous = None
                    i += 1
                    curr_ind = i

                j += 1
                continue

            active_edge = edge
            remaining = i - curr_ind + 1
            node_found = False

            # Skip count
            while remaining > len(active_edge):
                active_node = active_edge.next
                
                curr_ind += len(active_edge)
                remaining -= len(active_edge)

                active_edge = active_node.get_edge(st[curr_ind])

                # If rule 2 alternate is encountered during skip count
                if active_edge is None:
                    node_found = True
                    break
                     

            if node_found:
                continue

            # Index on active edge to compare with i 
            comp_ind = active_edge.start + remaining - 1 

            # Handle rule 3: showstopper
            # Moves to the next phase while freezing j till a rule 2 occurs
            if st[comp_ind] == st[i]:
                
                # Suffix link
                if previous is not None:
                    previous.link = active_node
                previous = None

                i += 1
                continue
                

            # Handle all rule 2 general cases
            node = self.create_new_node(active_edge, st, i, comp_ind, j)

            # Suffix link manipulation
            if previous is not None:
                previous.link = node
            previous = node

            # Reset curr_ind
            if active_node is self.root:
                curr_ind += 1

            # Suffix link traversal
            active_node = active_node.link            
            j += 1


    '''
    Called when a new internal node is being created. 
    '''
    def create_new_node(self, active_edge, st, i, comp_ind, j):
        node = Node()
        prev_path = Edge(comp_ind, active_edge.end, active_edge.suffix_id)
        node.set_edge(st[i], Edge(i, self.__global_end, j))
        node.set_edge(st[comp_ind], prev_path)  
        prev_path.next = active_edge.next
        node.link = self.root

        active_edge.end = End(comp_ind - 1)
        active_edge.next = node
        active_edge.suffix_id = None
        
        return node

    '''
    Generate a suffix array from a constructed suffix tree
    '''
    def generate_suffix_array(self):
        arr = []
        self.inorder_aux(self.root, arr)
        return arr
    

    def inorder_aux(self, node, arr):
        for edge in node.edges:
            if edge is None:
                continue

            if edge.next is None:
                arr.append(edge.suffix_id)
            else:
                self.inorder_aux(edge.next, arr)




# Suffix Tree components
# ===================================================================================================

'''
Each node maintains a list of edges connected to it
'''
class Node:
    def __init__(self, link=None):
        self.edges = [None]*ALPHABET_SIZE
        self.link = None

    def set_edge(self, char, edge):
        ind = ord(char) - ASCII_START
        self.edges[ind] = edge

    def get_edge(self, char):
        ind = ord(char) - ASCII_START
        return self.edges[ind]


'''
Edges stores the start and end indices, also the next node connected to it, 
if any. If the edge is a leaf, it will contain a non null suffix_id
'''
class Edge:
    def __init__(self, start, end, suffix_id = None):
        self.start = start
        self.end= end
        self.next = None
        self.suffix_id = suffix_id

    def __len__(self):
        return self.end.value - self.start + 1


'''
Class to keep track of global end since Python does not pass primitives by reference
'''
class End:
    def __init__(self, val=-1):
        self.value = val

    def set_value(self, val):
        self.value = val



# I/O operations
# ==================================================================================================

def open_file(filename):
    st = ""

    with open(filename, 'r') as file:
        for line in file:
            st += line.strip()

    return st

'''
Takes in a zero-indexed suffix array and writes to output file in 1-indexed form
'''
def write_output(suffix_array):
    n = len(suffix_array)

    with open(OUTPUT_FILE, 'w') as file:
        for i in range(n-1):
            file.write(f"{suffix_array[i]+1}\n")
        file.write(f"{suffix_array[-1]+1}")

           

if __name__ == "__main__":
    _, inputfile = sys.argv

    # It is assumed that all characters are within the ascii range [37, 126]
    text = open_file(inputfile)

    # Construct suffix tree using Ukkonen class
    ukkonen = Ukkonen(text)

    # Create suffix array from suffix tree: Inorder traversal
    suffix_array = ukkonen.generate_suffix_array()

    # Write output to file
    write_output(suffix_array)
   