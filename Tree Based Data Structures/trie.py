class Trie:

    def __init__(self):
        self.root = Node()
        self.count = 0
        self.height = 0

    '''
    Inserting a provided string and setting payload. If a duplicate is provided,
    the payload is updated
    '''
    def insert(self,key, data=None):
        current = self.root

        # Go through each char and create node if not already present
        for char in key:
            index = ord(char) - 97 + 1

            if current.link[index] is None:
                current.link[index] = Node()
            
            current = current.link[index]

        te_ind = Node.terminal_index

        if current.link[te_ind] is None:
            current.link[te_ind] = Node()

        current = current.link[te_ind]

        # Setting payload
        current.data = data
        self.count += 1

        if len(key) > self.height:
            self.height = len(key)


    '''
    If key is found, returns the payload. If not found, raises a KeyError
    '''
    def search(self, st):
        current = self.root

        for char in st:
            index = ord(char) - 97 + 1

            if current.link[index] is None:
                raise KeyError('Key not found')
            
            current = current.link[index]

        if current.link[0] is not None:
            return current.link[0].data
        else:
            raise KeyError('Key not found')
    

    '''
    Traverses over trie and returns a sorted list of all strings stored in the trie
    '''
    def __str__(self):
        node = self.root
        res = []
        self.str_aux(node, res)
        return res
            

    def str_aux(self, node,  res, arr=[]):
        for i in range(0, len(node.link)):
            elem = node.link[i]

            if elem is None:
                continue

            # Base
            if i == 0:
                res.append(''.join(arr))

            else:
            # Recursion
                value = chr(i + 97 - 1)
                self.str_aux(elem, res, arr.append(value))
                


class Node:
    terminal_index = 0

    def __init__(self, size=27):
        self.link = [None] * size
        self.data = None



if __name__ == "__main__":
    trie = Trie()




    
