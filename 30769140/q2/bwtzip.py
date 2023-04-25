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

    def __init__(self, text, writer):
        self.bwt, self.range_array = self.__construct_bwt_freq(text)
        self.bwt_unique_count = self.__generate_huffman_codes()
        self.writer = writer

    '''
    Constructs the Burrows-Wheeler transform for the provided text and creates 
    a list with the frequencies for each character
    '''
    def __construct_bwt_freq(self, text):
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

        bwt = ''.join(res)
        return bwt, freq_array


    '''
    Run after BWT construction. Creates a min heap and serves elements from it to
    create the huffman encoding for each unique character, which is recorded in 
    self.range_array
    Returns the number of unique character in the BWT
    '''
    def __generate_huffman_codes(self):
        heap = []
        unique_count = 0

        # Put elems in freq_array into a minheap as well as make note of number of 
        # unique elements
        for ind, elem in enumerate(self.range_array):
            if elem is None:
                continue

            freq = elem[0]      
            unique_count += 1     
            heapq.heappush(heap, (freq, [ind]))

        # Pop elems in heap twice at a time to form huffman codes
        while len(heap) >= 2:
            first = heapq.heappop(heap)
            second = heapq.heappop(heap)
            
            # Get frequencies and corresponding indices
            first_freq, second_freq = first[0], second[0]
            first_idx, second_idx = first[1], second[1]

            # Keep record of digit
            self.__append_huffman_digit(first_idx, 0)
            self.__append_huffman_digit(second_idx, 1)

            # Add cumulative freq to the heap
            heapq.heappush(heap, (first_freq + second_freq, first_idx + second_idx))

        return unique_count
    

    def __append_huffman_digit(self, idx_arr, digit):
        for idx in idx_arr:
            huffman_arr = self.range_array[idx][1]
            huffman_arr.append(digit)


    def __generate_elias_code(self, num):

        # Number is the code component
        code_cmp = num
        n = code_cmp.bit_length()

        # Result array with encoded components
        res = [f"{code_cmp:b}"]

        while n > 1:
            len_cmp = n -1

            # Bit length of length component
            n = len_cmp.bit_length()

            # Current length component
            len_cmp = len_cmp - 2**(n-1)

            res.append(f"{len_cmp:0{n}b}")

        # Complexity of reversed is O(1), join O(n)
        return ''.join(reversed(res))
    

    def __encode_header(self):
        # Length of bwt
        bwt_length = self.__generate_elias_code(len(self.bwt))

        # No of distinct bwt characters
        bwt_unique = self.__generate_elias_code(self.bwt_unique_count)

        header_elias = [bwt_length, bwt_unique]

        for elem in header_elias:
            writer.parse_elias(elem)

        # Huffman header:
        # 7 bit ascii, length of huffman codeword, huffman codeword

        for ind, elem in enumerate(self.range_array):
            if elem is None:
                continue

            ascii_code = ind + 37 - 1
            huffman = elem[1]
            huffman_len = len(huffman)
            print(ascii_code, huffman_len, huffman)
            
            
    '''
    Perform run length encoding
    '''
    def encode(self):
        writer.open_file()

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

        writer.close_file()


# Writing encoded output 
# ================================================================================

'''
FileWriter class to handle packing bits to bytes and writing to a provided file
'''
class FileWriter:
    BUFFER_SIZE = 8

    def __init__(self, filename):
        self.__buffer = [None] * FileWriter.BUFFER_SIZE
        self.__ptr = 0

        if filename is None:
            raise TypeError('Filename cannot be None')

        # File writing attributes
        self.__filename = filename 
        self.__file = None


    
    # Allow to change filename if no file is open
    def set_file(self, filename):
        if self.__file is not None:
            raise IOError('Close currently opened file')
        
        if filename is None:
            raise TypeError('Filename cannot be None')

        self.__filename = filename

    
    # Must be run before running file operations
    def open_file(self, filename=None):
        if self.__file is not None:
            raise IOError('Close currently opened file')
        
        if filename is not None:
            self.set_file(filename)

        self.__file = open(self.__filename, 'wb')

    
    #Must be called at the end of writing operation. Flushes contents of buffer if any
    # before closing file
    def close_file(self):
        self.__flush()
        if self.__file is not None:
            self.__file.close()

        self.__file = None


    # Given an elias code string, will write bit by bit to the file
    def parse_elias(self, st):
        if self.__file is None:
            raise IOError('File must be open')

        for elem in st:
            self.__add(elem)

    
    # Logic to maintain buffer and write bits to file once full
    def __add(self, bit):
        buffer = self.__buffer

        if self.__ptr >= FileWriter.BUFFER_SIZE:
            raise RuntimeError('Illegal state, buffer index should be within limits')

        buffer[self.__ptr] = bit
        self.__ptr += 1
        if self.__ptr >= FileWriter.BUFFER_SIZE:
            self.__flush()


    def parse_huffman(self):
        if self.__file is None:
            raise IOError('File must be open')

        pass
        

    # Writes to the file, one byte at a time. If the buffer is not full when called,
    # will pad remainder with zero bits.
    def __flush(self):
        if self.__file is None:
            raise IOError('File must be open')
        
        # Nothing to flush if buffer is empty
        if self.__ptr == 0:
            return
        
        # pad zeros if buffer not full when called
        while self.__ptr < FileWriter.BUFFER_SIZE:
            self.__buffer[self.__ptr] = '0'
            self.__ptr += 1

        bitstring = "".join(self.__buffer)
        num = int(bitstring, 2)
        byte = num.to_bytes(1, "big")

        print(byte)
        self.__file.write(byte)
        self.__ptr = 0


    
    # Cleans resources
    def __del__(self):
        if self.__file is not None:
            self.close_file()
        


# Reading input
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

    writer = FileWriter(OUTPUT_FILE)
    encoder = Encoder(text, writer)
    # encoder.generate_elias_code(561)
    # print(encoder.bwt)
    # print(encoder.freq_array)
    encoder.encode()


    # Strategy:
    # Generate huffman codes
    # Function to generate elias code
    # Research packing into binary
    # encode header
    # run length encode (simple loop)

    
