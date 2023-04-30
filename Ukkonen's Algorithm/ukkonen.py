ALPHABET_SIZE = 91
ASCII_START = 36

def ukkonen_naive_loop(st):
    st = st + "$"
    n = len(st)
    root = Node()

    # Loop over phases
    for i in range(n):
        j = 0
        # Loop over extensions
        while j <= i:
            chr = st[j]
            ind = ord(chr) - ASCII_START
            edge = root.edges[ind]

            if edge is None:
                root.edges[ind] = Edge(j, i)
                j+=1
                continue


            # Naive extension traversal
            # Something similar to skip count is going on here
            substr_len = i - j
            while len(edge) < substr_len:

                if edge.next is None:
                    break
                    
                else:
                    edge = edge.next
                    substr_len = i - edge.end

              # Case 1: Can remove this if we just used a global end
            edge.end += 1  
            j+= 1

            # Case 2 or 3





            ind = edge.start

            while ind < edge.end:
                st[ind]


            # Skip count optimization 
            # substr_len = i - j

        
            # if substr_len > edge.end:
                # Will have to jump to next edge (if any)
                # Only at the last edge can I determine the case
                # Much better to abstract global end so that I don't
                # have to worry about it
                # edge.end = i
            # else:
                # already at last edge
                # case 2 or 3 
                # traverse to the end and perform 
                # if truly optimized, can just compare the necessary
                # and perform extension
                





            j+= 1
            
            # Traversal
            pass


    return root
            

class Node:
    def __init__(self):
        self.edges = [None]*ALPHABET_SIZE

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end= end
        self.next = None

    def set_end(self, end):
        self.end = end


    def __len__(self):
        return self.end - self.start


if __name__ == "__main__":
    ukkonen_naive_loop("apple")

