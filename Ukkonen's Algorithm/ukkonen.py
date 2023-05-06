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
        self.root.link = self.root

        self.__global_end = End()
        self.run()


    def run(self):
        st = self.st + "$"
        n = len(st)

        i, j = 0, 0 # Initial phase and initial extension
        active_node = self.root
        active_edge = None
        curr_ind = j
        previous= None

        while i < n:
            self.__global_end.set_value(i)
            edge = active_node.get_edge(st[curr_ind])

            if edge is None:
                print(f"{j},{i} rule 2")
                active_node.set_edge(st[curr_ind], Edge(curr_ind, self.__global_end, j))
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
                previous = None
                print(f"{j},{i} rule 3")
                i += 1
                continue
                
            node = self.create_new_node(active_edge, st, i, comp_ind, j)
            
            print(f"{j},{i} rule 2")

            if previous is not None:
                previous.link = node

            previous = node
            if active_node is self.root:
                curr_ind += 1

            active_node = active_node.link

            
            # if j == i:
            #     print("I run")
            #     previous = None
            #     i += 1
            #     j += 1
            #     curr_ind = j
            #     continue
            
            j += 1

         



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


class Edge:
    def __init__(self, start, end, suffix_id = None):
        self.start = start
        self.end= end
        self.next = None
        self.suffix_id = suffix_id

    def __len__(self):
        return self.end.value - self.start + 1


if __name__ == "__main__":
    tests = ['abba', 'baab', 'abcab', 'acccb', 'googol', 'hatcat', 'aabcaba', 'abaaba', 'mississippi', 'abcabxabcyab', 'wolloomooloo']
    # ukkonen = Ukkonen("mississippi")
    # ukkonen = Ukkonen("abcabxazaby")
    # for test in tests:
    #     ukkonen = Ukkonen(test)
    #     suffix_array = ukkonen.generate_suffix_array()
    #     print(f"{test}: {suffix_array}")

    ukkonen = Ukkonen(tests[-1])
    suffix_array = ukkonen.generate_suffix_array()
    print(suffix_array)

