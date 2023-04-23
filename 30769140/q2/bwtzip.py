'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys
import heapq

OUTPUT_FILE = "bwtencoded.bin"
TERMINAL_CHAR = "$"
ASCII_RANGE = 91    # 126 - 37 + 2 (For terminal char and inclusive end)

def naive_suffix_array(text):
    arr = list(range(len(text))) #O(n)
    arr.sort(key = lambda x: text[x::]) # O(n* nlogn * comparison)

    return arr


class Encoder:

    def __init__(self, text):
        self.__construct_bwt(text)
        self.__generate_huffman_codes()


    def __construct_bwt(self, text):
        # Preprocess text
        text += TERMINAL_CHAR

        # Construct suffix array
        suffix_array = naive_suffix_array(text)  # Plug in efficient version here
        n = len(suffix_array)
        res = []

        freq_array = [None] * ASCII_RANGE

        # Loop over suffix array
        for elem in suffix_array:

            # Construct bwt
            ind = (elem - 1) % n
            char = text[ind]
            res.append(char)

            freq_ind = ord(char) - 37 + 1
            elem = freq_array[freq_ind]

            # Keep track of frequency
            if elem is None:
                freq_array[freq_ind] = (1, [])
            else:
                count = elem[0]
                freq_array[freq_ind] = (count + 1, [])

        self.bwt = ''.join(res)
        self.freq_array = freq_array  
    

    def __generate_huffman_codes(self):
        heap = []

        # loop through frequency array
        for ind, elem in enumerate(self.freq_array):
            if elem is None:
                continue

            freq = elem[0]
            ascii_val = ind + 37 - 1
            
            heapq.heappush(heap, (freq, [ascii_val]))

        print(heap)




    def __generate_elias_code(self, num):
        pass


    def __encode_header(self):
        # Length of bwt
        # No of distinct bwt characters
        # 7 bit ascii, length of huffman, huffman code
        pass

    '''
    Perform run length encoding
    '''
    def encode(self):
        self.__encode_header()

        st = self.bwt
        ind = 0

        while ind < len(st):
            count = 1

            while st[ind] == st[ind+count]:
                count += 1
                if count + ind >= len(st):
                    break 

            # Encode st[i]
            # Encode count
            print(st[ind], count)
            ind += count 
                    


# I/O operations
# ==============================================================

def open_file(filename):
    st = ""

    with open(filename, 'r') as file:
        for line in file:
            st += line.strip()

    return st


if __name__ == "__main__":
    _, filename = sys.argv

    # It is assumed that the file only contains characters
    # from the ascii range [37, 126]
    text = open_file(filename)

    encoder = Encoder(text)
    # print(encoder.bwt)
    # print(encoder.freq_array)
    # encoder.encode()


    # Strategy:
    # Generate huffman codes
    # Function to generate elias code
    # Research packing into binary
    # encode header
    # run length encode (simple loop)

    
