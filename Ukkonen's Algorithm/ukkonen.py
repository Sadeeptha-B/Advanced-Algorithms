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

        self.run()

    def run(self):
        st = self.st + "$"
        n = len(st)

        # Initialize extension, global end
        j = 0 
        active_node = self.root

        # Loop over phases
        for i in range(n):
            self.__global_end.increment()

            if j == i:
                #Final character, no one to compare
                ind = ord(st[j]) - ASCII_START
                edge = active_node.edges[ind]

                if edge is None:
                    active_node.edges[ind] = Edge(j, self.__global_end)
                    j += 1
                else:
                    active_edge = edge
                    active_len = 1

                continue

            while j < i:

                # Skip count traversal
                suffix_len = i - j + 1

                while suffix_len > len(active_edge):
                    # Next node
                    active_node = active_edge.next

                    # Subtract edge traversal
                    suffix_len -= len(active_edge)

                    # next suffix char
                    suffix_char =  st[j + len(active_edge)]

                    # next active_edge: this edge MUST be present because rule 1 extensions should already be covered
                    active_edge = active_node.edges[ord(suffix_char) - ASCII_START]

            



          




                # Next character to compare for case 3
                ext_char = st[i]
                edge_char = st[active_edge.start + active_len]







                




                
                
                pass








            
            # Loop over extensions
            while j <= i:
                char = st[j]
                ind = ord(char) - ASCII_START
                edge = active_node.edges[ind]   # Use active node instead

                if edge is None:
                    active_node.edges[ind] = Edge(j, self.__global_end)
                    # Will need to increment j or break out
                    continue

                suffix_len = i - j + 1

                while suffix_len > len(edge):
                    
                    # If larger, then jump to next node and make it active node

                    # If no node, will relate to leaf extension which should be already covered.
                    # This is not possible since j should be after all leaf extensions are already done
                    active_node = edge.next
                    # compare next
                    
                    



                # edge is not none
                # implement skip count
                # Once remainder of edge is reached, initiate rule 2 or rule 3
                # if rule 2 create suffix link back to root
                # next time active node will begin from there
                # If rule 3, set active node active length and active edge

            
                j += 1

            
            # Increment j along with i if not rule 3 
            # If rule 3 freeze
            j += 1
                

            # Rule 1
            self.__global_end.increment()

            

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
    def __init__(self):
        self.edges = [None]*ALPHABET_SIZE

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

