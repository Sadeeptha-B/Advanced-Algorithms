import math


class MinHeap:
    def __init__(self, array):
        self.heap = self.buildHeap(array)

    def buildHeap(self, array):
        n = len(array)

        if n <= 1:
            return array

        parent_ind = math.floor((n-2)/2)
        for i in range(parent_ind, -1, -1):
            self.siftDown(i, array)

        return array
    

    def siftDown(self, ind, array):
        left = 2*ind + 1
        right = 2*(ind +1)
        n = len(array)

        if left >= n:
            return 

        if right >= n:
            right = left

        # Get minimum child index
        min_child = left if array[left] <= array[right] else right       
       
        # Swap if parent larger and continue
        if array[ind] > array[min_child]:
            array[ind], array[min_child] = array[min_child], array[ind]
            self.siftDown(min_child, array)   
            

    def siftUp(self, ind):
        par_ind = math.floor((ind-1)/2)

        # Loop while parent is larger than child
        while ind > 0 and self.heap[par_ind] > self.heap[ind]:
            # swap
            self.heap[par_ind], self.heap[ind] = self.heap[ind], self.heap[par_ind]
            ind = par_ind
            par_ind = math.floor((par_ind-1)/2)
        

    def peek(self):
        if len(self.heap) <= 0:
            return None
        return self.heap[0]
            

    def remove(self):
        if len(self.heap) <= 0:
            return None

        # swap root and end
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        elem = self.heap.pop()

        self.siftDown(0, self.heap)
        return elem
        

    def insert(self, value):
        # Write your code here.
        self.heap.append(value)
        n = len(self.heap)
        self.siftUp(n-1)

        
    
