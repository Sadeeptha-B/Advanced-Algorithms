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
        self.root.id = 0
        self.run1()



    def run1(self):
        st = self.st + "$"
        n = len(st)

        j = 0 # Initial extension
        active_node = self.root
        active_edge = None
        curr_ind = j
        previous= None

        for i in range(n):
            self.__global_end.set_value(i)
            edge = active_node.get_edge(st[curr_ind])

            if edge is None:
                print(f"{j},{i} rule 2")
                active_node.set_edge(st[curr_ind], Edge(curr_ind, self.__global_end, j))
                j += 1
                curr_ind += 1
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
                    while j <= i:
                        print(f"{j}, {i} rule 2 alt")
                        active_edge = Edge(curr_ind, self.__global_end, j)
                        active_node.set_edge(st[curr_ind], active_edge)
                        active_node = active_node.link
                        j += 1
                     

            if node_found:
                previous = None
                curr_ind = j
                continue

            if i ==5:
                print(remaining)
            comp_ind = active_edge.start + remaining - 1 

            # Rule 3
            if st[comp_ind] == st[i]:
                print(f"{j},{i} rule 3")
                continue
                
            # Propagate rule 2
            while j <= i:
                node = self.create_new_node(active_edge, st, i, comp_ind, j)
                print(f"{j},{i} rule 2")
                if previous is not None:
                    previous.link = node
                
                previous = node
                active_node = active_node.link
                j += 1
                # print(j)
                if active_node is self.root:
                    curr_ind = j 
                    remaining = i - curr_ind - 1

                active_edge = active_node.get_edge(st[curr_ind])

                if active_edge is None:
                    print(f"{j}, {i} rule 2 alt:root")
                    active_node.set_edge(st[curr_ind], Edge(curr_ind, self.__global_end, j))
                    break

                comp_ind = active_edge.start + remaining - 1

                if st[comp_ind] == st[i]:
                    break

            # Reset before new phase
            previous = None
            curr_ind = j




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



    def run(self):
        st = self.st + "$"
        n = len(st)

        # Initialize extension index, active node
        j = 0 
        active_node = self.root
        suffix_len = 0
        node_count  = 1

        # Loop over phases
        for i in range(n):
            # Trick 1: Global end 
            self.__global_end.set_value(i)
                
            while j < i:
               
                # Trick 3: Skip count traversal
                char_ind = i - suffix_len + 1
                if j == 5 and i == 8:
                    print(char_ind, suffix_len, len(active_edge), (active_edge.start, active_edge.end.value))
                

                while suffix_len > len(active_edge):
                    # Next node: this MUST be present
                    active_node = active_edge.next

                    # Subtract edge traversal
                    suffix_len -= len(active_edge)

                    # next suffix char
                    char_ind += len(active_edge)
                    suffix_char =  st[char_ind]

                    # next active_edge
                    active_edge = active_node.edges[ord(suffix_char) - ASCII_START]
                    active_ptr = 0

                    # Rule 2 alt: rooted
                    if active_edge is None:
                        active_edge = Edge(char_ind, self.__global_end, j)
                        active_node.edges[ord(suffix_char) - ASCII_START] = active_edge


                    skip_count = True
                    # Rule 2 alternate: Suffix link
                    # if active_edge is None:
                    #     active_edge = Edge(char_ind, self.__global_end, j)
                    #     while j < i:
                    #         print(f"{j}, {i} rule 2 alt")
                    #         active_node.edges[ord(suffix_char) - ASCII_START] = active_edge
                    #         active_node = active_node.link
                    #         # print(node.id)
                    #         print(node.id)
                    #         print("=======")
                            
                    #         j += 1
                
                if active_edge.start == i:
                    print(f"{j}, {i} rule 2 alt")
                    active_node = active_node.link
                    active_ptr = 1
                    j += 1
                    active_edge = active_node.edges[ord(st[j]) - ASCII_START]
                    suffix_len = i - j + 1
                    continue
                    
                          
                if j == i:
                    break
      

                # After skip count traversal: case 2 or case 3 must occur    
                # Comparing the suffix extension char and the edge character
                comp_ind = active_edge.start + active_ptr 
                edge_char = st[comp_ind]       
                extension = st[i]

                # Rule 3
                if extension == edge_char:
                    print(f"{j}, {i} rule 3")

                    active_ptr += 1
                    suffix_len += 1
                  
                    break


                # Rule 2: General
                print(f"{j}, {i} rule 2 gen")

                node = Node()    
                node.id = node_count 
                node_count += 1
                node.edges[ord(extension) - ASCII_START] = Edge(i, self.__global_end, j)
                node.edges[ord(edge_char) - ASCII_START] = Edge(comp_ind, active_edge.end, active_edge.suffix_id)
                node.link = self.root

                # Wiring up active_edge
                active_edge.end = End(comp_ind - 1)
                node.edges[ord(edge_char) - ASCII_START].next = active_edge.next
                active_edge.next = node
                active_edge.suffix_id = None


                # Preparing for next extension
                active_node = active_node.link
                active_ptr = 1
                suffix_len -= 1
                j += 1
                active_edge = active_node.edges[ord(st[j]) - ASCII_START] 

                if active_node == self.root:
                    suffix_len = i - j + 1


            if j == i:
                ind = ord(st[j]) - ASCII_START
                edge = self.root.edges[ind]

                # Rule 2 alternate
                if edge is None:
                    # Trick 2: start, end representation
                    print(f"{j}, {i} rule 2 alt:root")
   
                    self.root.edges[ind] = Edge(j, self.__global_end, j)
                    j += 1
                else:
                    print(f"{j}, {i} rule 3")
                    active_edge = edge
                    active_ptr = 1
                    suffix_len = 1 + active_ptr


        
        

    def generate_suffix_array(self):
        arr = []
        self.inorder_aux(self.root, arr)
        return arr
    
    def inorder_aux(self, node, arr):
        for edge in node.edges:
            if edge is None:
                continue

            if edge.next is None:
                # print(edge.start, edge.end.value, edge.suffix_id)
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
        self.id = None

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
    print(len("abcabxazaby$"))
    print("=====")

    ukkonen = Ukkonen("mississippi")
    # ukkonen = Ukkonen("abcabxazaby")
    # ukkonen = Ukkonen("abcabxazabyabcyab")


    suffix_array = ukkonen.generate_suffix_array()
    print(suffix_array)

