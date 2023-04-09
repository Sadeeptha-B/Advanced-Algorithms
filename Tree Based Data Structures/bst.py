class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        node = self

        while node is not None:
            node_val = node.value

            if value < node_val:
                next = node.left
                if next is None:
                    node.left = BST(value)
                
            elif value >= node_val:
                next = node.right
                if next is None:
                    node.right = BST(value)
                    
            node = next
            
        return self

    def contains(self, value):
        node = self

        while node is not None:
            node_val = node.value

            if value == node_val:
                return True
            elif value < node_val:
                next = node.left
            else:
                next = node.right

            node = next

        return False
                

    def remove(self, value, parent=None):
        current = self

        while current is not None:
            if value < current.value:
                parent = current
                current = current.left
                
            elif value > current.value:
                parent = current
                current = current.right
                
            else:
                if current.left is not None and current.right is not None:
                    current.value = current.right.getMinValue()
                    current.right.remove(current.value, current) # Passing the parent is important to set the parent properly
                elif parent is None:
                    if current.left is not None:
                        current.value = current.left.value
                        current.right = current.left.right
                        current.left = current.left.left
                    elif current.right is not None:
                        current.value = current.right.value
                        current.left = current.right.left
                        current.right = current.right.right
                    # else:
                    #     current.value = None # No tree at all
                elif parent.left is current:
                    parent.left = current.left if current.left is not None else current.right
                elif parent.right is current:
                    parent.right = current.left if current.left is not None else current.right
                break
                                       
        return self


    def getMinValue(self):
        node = self

        # Function will be called on a non-none node, as such will be looped at least once
        while node.left is not None:
            node = node.left

        return node.value


        