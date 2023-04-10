class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, st):
        current = self.root

        for char in st:
            index = ord(char) - 97 + 1

            if current.link[index] is None:
                current.link[index] = Node()
            
            current = current.link[index]

        current.link[0] = Node()
    
    def search(self, st):
        current = self.root

        for char in st:
            index = ord(char) - 97 + 1

            if current.link[index] is None:
                return False
            
            current = current.link[index]

        return current.link[0] is not None
    
    '''Gives a sorted list of all strings stored in the trie'''
    def __str__(self):
        pass




class Node:
    def __init__(self, size=27):
        self.link = [None] * size
        self.value = None



if __name__ == "__main__":
    pass
    
