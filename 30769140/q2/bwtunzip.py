'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = 'recovered.txt'
BYTE_SIZE = 8 # 1 byte is 8 bits
ASCII_HEADER_SIZE = 7
ASCII_RANGE = 91
ASCII_START = 36
TERMINAL_CHAR = "$"

'''
For use in Binary tree
'''        
class Node:
    def __init__(self):
        self.elem_ascii = None
        self.link = [None, None]


'''
Makes use of BinaryReader to read the binary file bit by bit and decodes 
the header and data
'''
class Decoder:
    def __init__(self, reader):
        self.reader = reader
        self.bwt_length = 0
        self.unique_bwt = 0
        self.__huffman_root = Node()


    '''
    Drives the decoding algorithm
    '''
    def decode(self):
        reader.open_file()

        try:
            self.process_header()
        except IOError as e:
            print('Invalid file. Ran out of bits while processing header')
        else:
            data = self.__decode_data()
            txt = self.invert_bwt(data)
        finally:
            reader.close_file()

        return txt


    '''
    Run after the header is read. Decodes the data fully, according to runlength
    decoding. Throws exceptions if file ends prematurely or unknown huffman code is
    encountered
    '''
    def __decode_data(self):
        res = []

        while len(res) < self.bwt_length:
            char = self.decode_huffman()
            char_count = self.decode_elias()
            
            for _ in range(char_count):
                res.append(char)

        return ''.join(res)


    '''
    Processes the header. Throws exceptions if file ends prematurely.
    '''
    def process_header(self):
        self.bwt_length = self.decode_elias()
        self.unique_bwt = self.decode_elias()


        # Decode bwt characters and ascii encodings
        for _ in range(self.unique_bwt):
            ascii_code = self.decode_ascii()
            huffman_len = self.decode_elias()
            huffman_lst = reader.read_bits(huffman_len)

            if len(huffman_lst) != huffman_len:
                raise IOError('No more bits to read')

            self.__construct_huffman_tree(ascii_code, huffman_lst)


    '''
    Provided the ascii code and a list of bits will add code to the tree
    '''
    def __construct_huffman_tree(self, ascii_code, huffman_lst):
        node = self.__huffman_root

        for elem in huffman_lst:
            elem = int(elem)

            if node.link[elem] is None:
                node.link[elem] = Node()

            node = node.link[elem]

        node.elem_ascii = ascii_code


    '''
    Traverse constructed huffman tree and get relevant ascii character
    '''
    def decode_huffman(self):
        node = self.__huffman_root

        while node.elem_ascii is None:
            bit = reader.read_bit()
            if bit is None:
                raise IOError('Ran out of bits while decoding')
            
            next = node.link[bit]

            if next is None:
                raise ValueError('Unknown huffman code')
            
            node = next
        
        return chr(node.elem_ascii)


    '''
    Reads bits from file as appropriate to decode elias code.
    '''
    def decode_elias(self):
        num = 0

        while True:
            bit_count = num + 1
            bitstr = reader.read_bitstr(bit_count)

            if len(bitstr) != bit_count:
                raise IOError('No more bits to read')
            
            mask = 1 << (bit_count - 1)
            num = int(bitstr, 2) | mask

            if  bitstr[0] == "1":
                break

        return num
        
    '''
    Reads header size ascii bits and returns relevant codepoint.
    '''
    def decode_ascii(self):
        ascii_bits = reader.read_bitstr(ASCII_HEADER_SIZE)

        if len(ascii_bits) != ASCII_HEADER_SIZE:
            raise IOError('No more bits to read')

        return int(ascii_bits, 2)
    

    def invert_bwt(self, bwt):
        n = len(bwt) - 1
        res = [None] * n 

        rank, occ = self.__compute_rank_occ(bwt) # O(n)

        i = n - 1
        next_i = 0
        char = bwt[next_i]

        '''
        Constructs the results array one by one by going back through the string
        '''
        while char != TERMINAL_CHAR:
            res[i] = char
            next_i = rank[ord(char) - ASCII_START] + occ[next_i]
            char = bwt[next_i]
            i -= 1
        
        return ''.join(res)
    
    def __compute_rank_occ(self, bwt):
        arr = [None]*ASCII_RANGE
        occ = [None]* len(bwt)

        # Calculate the count of each character occurence
        for i, char in enumerate(bwt):
            if char == TERMINAL_CHAR:
                arr[0] = 1
                occ[i] = 0
                continue

            ind = ord(char) - ASCII_START
            
            if arr[ind] is None:
                arr[ind] = 1
                occ[i] = 0
            else:
                occ[i] = arr[ind]
                arr[ind] += 1
        

        # Maintain a running count to keep track of rank
        run_count = 0
        for i in range(len(arr)):

            if arr[i] is not None:
                value = arr[i]
                arr[i] = run_count
                run_count += value
                
        return arr, occ

       
            

'''
BinaryReader class to handle the logic of reading bytes and unpacking bits.
Provides read_bit, read_bitarray, read_bits, read_bitstr methods.
'''
class BinaryReader: 
    CHUNK_SIZE = 1

    def __init__(self, filename):        
        if filename is None:
            raise ValueError('Filename cannot be None')

        self.__filename = filename
        self.__file = None
        self.__bitptr = 0
        self.__bitarray = None


    # Allow to change the filename if not file is open
    def set_file(self, filename):
        if self.__file is not None:
            raise IOError('Close currently opened file')
        
        if filename is None:
            raise ValueError('Filename cannot be None')

        self.__filename = filename


    # Must be run before running file operations
    def open_file(self, filename=None):
        if self.__file is not None:
            raise IOError('Close currently opened file')
        
        if filename is not None:
            self.set_file(filename)

        self.__file = open(self.__filename, 'rb')


    # Must be called at the end of writing operation
    def close_file(self):
        self.__bitptr = 0
        if self.__file is not None:
            self.__file.close()

        self.__file = None


    '''
    Handles the logic of reading a byte from a file and delegates to __parse_byte method
    to construct a bitarray

    - If called while buffer is not empty, it will not read anything
    - bitarray will be set to an empty list if there are no further bytes to read
    - Does not return anything. To access the bit_array, use get_bitarray method
    '''
    def read_bitarray(self):
        if self.__file is None:
            raise IOError("File needs to be open first")
        
        if 0 < self.__bitptr < BYTE_SIZE:
            return 

        file = self.__file
        byte = file.read(BinaryReader.CHUNK_SIZE) # Read 1 byte

        zeros, num = 0, 0

        if byte:
            num = ord(byte)
            zeros = BYTE_SIZE - num.bit_length()

        self.__bitarray = self.__parse_byte((zeros, num)) 
        self.__bitptr = 0

    '''
    Constructs and returns a bitarray when provided a tuple of the form
    (no of pad zeros, number)
    '''
    def __parse_byte(self, byte_tup):
        zeros, num = byte_tup
        bitarray = []

        for _ in range(zeros):
            bitarray.append(0)

        shift_bit = num.bit_length() - 1

        for _ in range(num.bit_length()):
            start = num >> shift_bit
            lsb = start % 2
            bitarray.append(lsb)
            shift_bit -= 1

        return bitarray

    '''
    Serves next bit according to bitptr. If the buffer end is reached,
    it is refilled, until end of file.
    Returns None if no further bits to read
    '''
    def read_bit(self):
        if self.__bitarray is None:
            self.read_bitarray()

        if self.__bitptr >= BYTE_SIZE:
            raise RuntimeError('Pointer cannot exceed bitarray bounds')

        if len(self.__bitarray) == 0:
            return None
        
        bit = self.__bitarray[self.__bitptr]
        self.__bitptr += 1

        if self.__bitptr >= BYTE_SIZE:
            self.read_bitarray()

        return bit
    
    '''
    Will read and return a list of specified amount of bits
    '''
    def read_bits(self, count):
        bits = []
        for _ in range(count):
            bit = self.read_bit()
            if bit is not None:
                bits.append(str(bit))

        return bits
    
    '''
    Return a string of upcoming bits of the specified length
    '''
    def read_bitstr(self, count):
        bits = self.read_bits(count)
        return ''.join(bits)
    

    '''
    Provide the bitarray if required
    '''
    def get_bitarray(self):
        if self.__bitarray is None:
            return []
        return list(self.__bitarray)


    # Cleans up resources 
    def __del__(self):
        if self.__file is not None:
            self.close_file()
        


if __name__ == "__main__":
    _, encodedfile = sys.argv

    reader = BinaryReader(encodedfile)
    decoder = Decoder(reader)
    txt = decoder.decode()

    # Write to output file
    with open(OUTPUT_FILE, 'w') as file:
        file.write(txt)

