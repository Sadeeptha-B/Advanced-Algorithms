ALPHABET_SIZE = 91
ASCII_START = 36

class Ukkonen:
    def __init__(self, st):
        self.st = st
        self.root = Node()
        self.__globalend = End()

        self.run()

    def run(self):
        st = self.st + "$"
        n = len(st)

        # Initialize extension, global end
        j = 0 
        global_end = self.__globalend
        global_end.set_value(0)
        active_node = self.root


        # Loop over phases
        for i in range(n):
            
            # Loop over extensions
            while j <= i:
                char = st[j]
                ind = ord(char) - ASCII_START
                edge = active_node.edges[ind]   # Use active node instead

                if edge is None:
                    self.root.edges[ind] = Edge(j, global_end)
                    continue

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
            global_end.increment()

            

    def generate_suffix_array(self):
        arr = []
        return arr

      
'''
Class to keep track of global end since Python does not pass values by reference
'''
class End:
    def __init_(self):
        self.end = None

    def set_value(self, value):
        self.end = value

    def increment(self, value=1):
        self.end += value


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
        return self.end - self.start + 1


if __name__ == "__main__":
    ukkonen = Ukkonen("abcabxabcyab")
    suffix_array = ukkonen.generate_suffix_array()
    print(suffix_array)

