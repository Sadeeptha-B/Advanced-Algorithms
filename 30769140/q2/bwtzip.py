'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = "bwtencoded.bin"
TERMINAL_CHAR = "$"
ASCII_RANGE = 91    # 126 - 37 + 2 (For terminal char and inclusive end)

def naive_suffix_array(text):
    arr = list(range(len(text))) #O(n)
    arr.sort(key = lambda x: text[x::]) # O(n* nlogn * comparison)

    return arr


class Encoder:

    def __init__(self, text):
        self.bwt = self.__construct_bwt(text)
        self.__generate_huffman_codes()


    def __construct_bwt(self, text):
        text += TERMINAL_CHAR
        suffix_array = naive_suffix_array(text)  # Plug in efficient version here
        n = len(suffix_array)
        res = []

        for elem in suffix_array:
            ind = (elem - 1) % n
            res.append(text[ind])

        return ''.join(res)
    

    def __generate_huffman_codes(self):
        freq_array = [None] * ASCII_RANGE

        for char in self.bwt:
            if char == "$":
                freq_array[0] = 1
                continue

            ind = ord(char) - 37 + 1

            if freq_array[ind] is None:
                freq_array[ind] = 1
            else:
                freq_array[ind] += 1

    '''
    Perform run length encoding
    '''
    def encode(self):
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
    print(encoder.bwt)
    encoder.encode()


    # Strategy:
    # Generate huffman codes
    # Function to generate elias code
    # Research packing into binary
    # encode header
    # run length encode (simple loop)

    
