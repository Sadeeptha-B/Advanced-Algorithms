class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self,key, data):
        current = self.root

        for char in key:
            index = ord(char) - 97 + 1

            if current.link[index] is None:
                current.link[index] = Node()
            
            current = current.link[index]

        te_ind = Node.TE_IND

        if current.link[te_ind] is None:
            current.link[te_ind] = Node()

        current = current.link[te_ind]
        current.data = data


    def search(self, st):
        current = self.root

        for char in st:
            index = ord(char) - 97 + 1

            if current.link[index] is None:
                return False
            
            current = current.link[index]

        if current.link[0] is not None:
            return current.link[0].data
        else:
            return False
    

    '''Gives a sorted list of all strings stored in the trie'''
    def __str__(self):
        node = self.root

        for i in range(len(node.link)):
            pass
            


class Node:

    TE_IND = 0

    def __init__(self, size=27):
        self.link = [None] * size
        self.data = None



if __name__ == "__main__":
    pass
    
