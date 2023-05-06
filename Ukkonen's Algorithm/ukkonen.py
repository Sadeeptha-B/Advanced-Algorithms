from typing import List


ALPHABET_SIZE = 91
ASCII_START = 36


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
        st = self.st + "$"
        n = len(st)

        # Initial phase and initial extension
        i, j = 0, 0 
        active_node = self.root
        active_edge = None
        curr_ind = j
        previous= None

        while i < n:
            self.__global_end.set_value(i)
            edge = active_node.get_edge(st[curr_ind])

            if edge is None:
                active_node.set_edge(st[curr_ind], Edge(curr_ind, self.__global_end, j))
                if previous is not None:

                    previous.link = active_node
                    previous = None
                
                active_node = active_node.link

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

                if active_edge is None:
                    node_found = True
                    break
                     

            if node_found:
                continue


            comp_ind = active_edge.start + remaining - 1 

            # Rule 3
            if st[comp_ind] == st[i]:
                if previous is not None:
                    previous.link = active_node
                previous = None
                i += 1
                continue
                
            node = self.create_new_node(active_edge, st, i, comp_ind, j)

            if previous is not None:
                previous.link = node

            previous = node
            if active_node is self.root:
                curr_ind += 1

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



'''
Class to keep track of global end since Python does not pass values by reference
'''
class End:
    def __init__(self, val=-1):
        self.value = val

    def set_value(self, val):
        self.value = val



# Suffix tree components
# ===============================================================================================

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
Class to keep track of global end since Python does not pass primitives by reference
'''
class Edge:
    def __init__(self, start, end, suffix_id = None):
        self.start = start
        self.end= end
        self.next = None
        self.suffix_id = suffix_id

    def __len__(self):
        return self.end.value - self.start + 1




def suffix_array_naive(word: str) -> List[int]:
    word = word + "$"
    arr = list(range(len(word))) #O(n)
    arr.sort(key = lambda x: word[x::]) # O(n* nlogn * comparison)
    return arr



def suffix_array_ukkonen(word: str) -> List[int]:
    # slave away for hours and put your code here
    ukkonen = Ukkonen(word)
    return ukkonen.generate_suffix_array()
    

if __name__ == "__main__":
    # allowable chars:
    chars = "abcdef"
    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                print('█', end="", flush=True)  # progress bar so you know if your code hung or not
                for c4 in chars:
                    for c5 in chars:
                        for c6 in chars:
                            for c7 in chars:
                                for c8 in chars:
                                    word = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 
                                    try:
                                        ukk = suffix_array_ukkonen(word)
                                        naive = suffix_array_naive(word)
                                        assert(ukk == naive)
                                    except AssertionError:
                                        print(f"Error on {word}")
                                        print(f"\tukkonen:\t {ukk}")
                                        print(f"\tnaive:\t\t {naive}")
    print("success")

