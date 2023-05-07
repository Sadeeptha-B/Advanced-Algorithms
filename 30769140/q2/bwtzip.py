'''
Author: Sadeeptha Bandara
Student ID: 30769140

Hello :) I expect the encoder to work without issue, but if there is any issue due 
to using Ukkonen for suffix array construction, please be kind enough to test with the 
provided naive_suffix_array implementation to check if the Encoder behaves as expected.
'''

import sys
import heapq


OUTPUT_FILE = "bwtencoded.bin"
TERMINAL_CHAR = "$"
ALPHABET_SIZE = 91    # 126 - 37 + 2 (For terminal char and inclusive end)
ASCII_START = 36
ASCII_HEADER_SIZE = 7

def naive_suffix_array(text):
    text = text + TERMINAL_CHAR
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
 
        # Construct suffix array
        ukkonen = Ukkonen(text)
        suffix_array = ukkonen.generate_suffix_array()
        # suffix_array = naive_suffix_array(text)

        text = text + TERMINAL_CHAR
        n = len(suffix_array)
        res = []

        freq_array = [None] * ALPHABET_SIZE

        # Loop over suffix array
        for elem in suffix_array:

            # Construct bwt

            ind = (elem - 1) % n
            char = text[ind]
            res.append(char)

            freq_ind = ord(char) - ASCII_START
            elem = freq_array[freq_ind]

            # Keep track of frequency
            if elem is None:
                freq_array[freq_ind] = (1, [])
            else:
                count = elem[0]
                freq_array[freq_ind] = (count + 1, elem[1])

        bwt = ''.join(res)
        return bwt, freq_array


    '''
    Run after BWT construction. Creates a min heap and serves elements from it to
    create the huffman encoding for each unique character, which is recorded in 
    self.range_array.

    The huffman encoding is stored in the form ['1', '1', '0'] corresponding to a huffman code
    of 011. So, the stored code must be reversed during processing

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
            self.__append_huffman_digit(first_idx, '0')
            self.__append_huffman_digit(second_idx, '1')

            # Add cumulative freq to the heap
            heapq.heappush(heap, (first_freq + second_freq, first_idx + second_idx))

        return unique_count
    
    '''
    Given a list of indices corresponding to ascii characters, appends relevant digit to keep 
    record of huffman encoding
    '''
    def __append_huffman_digit(self, idx_arr, digit):
        for idx in idx_arr:
            huffman_arr = self.range_array[idx][1]
            huffman_arr.append(digit)


    '''
    Generates the elias code for a provided integer.
    Returns a list of the form 
    [code_cmp, len_cmp1, len_cmp2....]
    The list needs to be reversed during processing.
    Each len_cmp is of the form (no of zero bits in front, len_component)
    '''
    def __generate_elias_code(self, num):
        if not isinstance(num, int):
            raise ValueError('num must be an integer')
    
        # Number is the code component
        code_cmp = num
        n = code_cmp.bit_length()

        # Result array with encoded components
        res = [num]

        while n > 1:
            len_cmp = n -1

            # Bit length of length component
            n = len_cmp.bit_length()

            # Current length component
            len_cmp = len_cmp - 2**(n-1)

            res.append((n - len_cmp.bit_length(), len_cmp))

        return res
    
    '''
    Encodes a header of the specification
    1. Length of bwt
    2. No of unique characters in bwt
    3. For each huffman character: 7 bit ascii representation, length of huffman code, huffman code word
    
    '''
    def __encode_header(self):
        # Length of bwt
        bwt_length = self.__generate_elias_code(len(self.bwt))

        # No of distinct bwt characters
        bwt_unique = self.__generate_elias_code(self.bwt_unique_count)

        header_elias = [bwt_length, bwt_unique]

        for elem in header_elias:
            writer.parse_elias(elem)

        # Huffman header
        for ind, elem in enumerate(self.range_array):
            if elem is None:
                continue

            # 7 bit ascii
            ascii_code = ind + ASCII_START
            writer.parse_int(ascii_code, ASCII_HEADER_SIZE)

            # Len of huffman code in elias
            huffman_len = self.__generate_elias_code(len(elem[1]))
            writer.parse_elias(huffman_len)

            # huffman codeword
            writer.parse_huffman(elem[1])    

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

            # Write huffman codeword
            freq_ind = ord(st[ind]) - ASCII_START
            writer.parse_huffman(self.range_array[freq_ind][1])

            # Encode count in elias
            writer.parse_elias(self.__generate_elias_code(count))

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
        # Buffer is filled with either 0 or 1 single char strings
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

    
    # Must be called at the end of writing operation. Flushes contents of buffer if any
    # before closing file
    def close_file(self):
        self.__flush()
        if self.__file is not None:
            self.__file.close()

        self.__file = None


    # Given an bitstring, will write bit by bit to the file
    def parse_bitstr(self, st):
        if self.__file is None:
            raise IOError('File must be open')

        for elem in st:
            self.add(elem)


    # Given a integer, will write it to in binary form to the file. If the total bits is specified, will pad bits in front
    def parse_int(self, num, total_bits=None):
        if not isinstance(num, int):
            raise ValueError('Num must be an int')

        bits  = num.bit_length()

        if total_bits is not None and total_bits > bits:
            diff = total_bits - bits
            for _ in range(diff):
                self.add('0')

        while bits > 0:
            start = num >> (bits - 1)
            msb = start % 2
            bits -= 1
            self.add(str(msb))

    # Takes an elias list as formatted in generate_elias_code in Encoder.
    def parse_elias(self, elias_lst):
        if self.__file is None:
            raise IOError('File must be open')
        
        for i in range(len(elias_lst)-1, -1, -1):
            elem = elias_lst[i]

            if isinstance(elem, tuple):
                zeros = elem[0]
                for _ in range(zeros):
                    self.add('0')
                cmp = elem[1]
            else:
                cmp = elem

            self.parse_int(cmp)

    
    # Logic to maintain buffer and write bits to file once full
    def add(self, bit):
        buffer = self.__buffer

        if self.__ptr >= FileWriter.BUFFER_SIZE:
            raise RuntimeError('Illegal state, buffer index should be within limits')

        buffer[self.__ptr] = bit
        self.__ptr += 1
        if self.__ptr >= FileWriter.BUFFER_SIZE:
            self.__flush()


    # Given a huffman list of the form [last digit, ...first digit]
    # will write bits in reverse order
    def parse_huffman(self, huffman_lst):
        if self.__file is None:
            raise IOError('File must be open')

        for i in range(len(huffman_lst)-1, -1, -1):
            self.add(huffman_lst[i])
            

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

        self.__file.write(byte)
        self.__ptr = 0
    
    
    # Cleans resources
    def __del__(self):
        if self.__file is not None:
            self.close_file()
        

# ===================================================================
# 
# Ukkonen implementation. Same as Q1
# Put here in case of any import issues
#
# ===================================================================


'''
Ukkonen class
'''
class Ukkonen:
    def __init__(self, st):
        self.st = st
        self.root = Node()
        self.root.link = self.root

        self.__global_end = End()
        self.run()


    '''
    Builds suffix tree in phases. In each phase i, constructs the implicit 
    suffix tree for [0..i] (0 based indexing).
    '''
    def run(self):
        st = self.st + TERMINAL_CHAR
        n = len(st)

        # Initialisation
        i, j = 0, 0 
        active_node = self.root
        active_edge = None
        curr_ind = j
        previous= None

        # Loop over phases
        while i < n:

            # Maintain global end
            self.__global_end.set_value(i)
            edge = active_node.get_edge(st[curr_ind])

            # Handle all rule 2 alternate cases
            if edge is None:
                active_node.set_edge(st[curr_ind], Edge(curr_ind, self.__global_end, j))
                
                # Suffix link manipulation
                if previous is not None:
                    previous.link = active_node
                    previous = None
                active_node = active_node.link

                # Move to next phase
                if i == j:
                    previous = None
                    i += 1
                    curr_ind = i

                j += 1
                continue

            active_edge = edge
            remaining = i - curr_ind + 1
            node_found = False

            # Skip count
            while remaining > len(active_edge):
                active_node = active_edge.next
                
                curr_ind += len(active_edge)
                remaining -= len(active_edge)

                active_edge = active_node.get_edge(st[curr_ind])

                # If rule 2 alternate is encountered during skip count
                if active_edge is None:
                    node_found = True
                    break
                     

            if node_found:
                continue

            # Index on active edge to compare with i 
            comp_ind = active_edge.start + remaining - 1 

            # Handle rule 3: showstopper
            # Moves to the next phase while freezing j till a rule 2 occurs
            if st[comp_ind] == st[i]:
                
                # Suffix link
                if previous is not None:
                    previous.link = active_node
                previous = None

                i += 1
                continue
                

            # Handle all rule 2 general cases
            node = self.create_new_node(active_edge, st, i, comp_ind, j)

            # Suffix link manipulation
            if previous is not None:
                previous.link = node
            previous = node

            # Reset curr_ind
            if active_node is self.root:
                curr_ind += 1

            # Suffix link traversal
            active_node = active_node.link            
            j += 1


    '''
    Called when a new internal node is being created. 
    '''
    def create_new_node(self, active_edge, st, i, comp_ind, j):
        node = Node()
        prev_path = Edge(comp_ind, active_edge.end, active_edge.suffix_id)
        node.set_edge(st[i], Edge(i, self.__global_end, j))
        node.set_edge(st[comp_ind], prev_path)  
        prev_path.next = active_edge.next
        node.link = self.root

        active_edge.end = End(comp_ind - 1)
        active_edge.next = node
        active_edge.suffix_id = None
        
        return node

    '''
    Generate a suffix array from a constructed suffix tree
    '''
    def generate_suffix_array(self):
        arr = []
        self.inorder_aux(self.root, arr)
        return arr
    

    def inorder_aux(self, node, arr):
        for edge in node.edges:
            if edge is None:
                continue

            if edge.next is None:
                arr.append(edge.suffix_id)
            else:
                self.inorder_aux(edge.next, arr)




# Suffix Tree components
# ===================================================================================================

'''
Each node maintains a list of edges connected to it
'''
class Node:
    def __init__(self, link=None):
        self.edges = [None]*ALPHABET_SIZE
        self.link = None

    def set_edge(self, char, edge):
        ind = ord(char) - ASCII_START
        self.edges[ind] = edge

    def get_edge(self, char):
        ind = ord(char) - ASCII_START
        return self.edges[ind]


'''
Edges stores the start and end indices, also the next node connected to it, 
if any. If the edge is a leaf, it will contain a non null suffix_id
'''
class Edge:
    def __init__(self, start, end, suffix_id = None):
        self.start = start
        self.end= end
        self.next = None
        self.suffix_id = suffix_id

    def __len__(self):
        return self.end.value - self.start + 1


'''
Class to keep track of global end since Python does not pass primitives by reference
'''
class End:
    def __init__(self, val=-1):
        self.value = val

    def set_value(self, val):
        self.value = val



# Reading input
# ==============================================================

def read_file(filename):
    st = ""

    with open(filename, 'r') as file:
        for line in file:
            st += line.strip()

    return st


# Runner
if __name__ == "__main__":
    _, filename = sys.argv

    # It is assumed that the file only contains characters
    # from the ascii range [37, 126]
    text = read_file(filename)

    writer = FileWriter(OUTPUT_FILE)
    encoder = Encoder(text, writer)
    encoder.encode()

    
