import math

class MinHeap:
    def __init__(self, array):
        self.heap = self.buildHeap(array)

    def buildHeap(self, array):
        # Write your code here.
        pass

    def siftDown(self):
        # Write your code here.
        pass

    def siftUp(self):
        ind = len(self) - 1
        heap = self.heap

        while ind >= 2:
            parent_ind =  math.floor((ind -1)/2)
            left = parent_ind * 2 + 1
            right = (parent_ind + 1) * 2 

            if right >= len(self):
                if heap[parent_ind] > heap[left]:
                    heap[parent_ind], heap[left] = heap[left], heap[parent_ind]
                    ind -= 1
                    continue

            min_child = heap[left]

            if heap[left]> heap[right]:
                min_child = heap[right]

            if heap[parent_ind] > heap[min_child]:
                heap[parent_ind], heap[min_child] = heap[min_child], heap[parent_ind]

            ind -= 1
            

    def peek(self):
        # Write your code here.
        if len(self.heap) <= 0:
            return None

        return self.heap[0]
            

    def remove(self):
        # Write your code here.
        pass

    def insert(self, value):
        # Write your code here.
        self.heap.append(value)
        self.siftUp()

    def __len__(self):
        return len(self.heap)
