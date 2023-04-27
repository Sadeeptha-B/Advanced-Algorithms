import sys

OUTPUT_FILE = 'recovered.txt'
BYTE_SIZE = 8 # 1 byte is 8 bits
ASCII_HEADER_SIZE = 7

class Decoder:
    def __init__(self, reader):
        self.reader = reader
        self.bwt_length = 0
        self.unique_bwt = 0

    def decode(self):
        reader.open_file()
        self.process_header()
        
        # Decode data by traversing huffman tree


        reader.close_file()


    def process_header(self):
        self.bwt_length = self.decode_elias()
        self.unique_bwt = self.decode_elias()

        print(self.bwt_length, self.unique_bwt)

        # Decode bwt characters and ascii encodings
        for _ in range(self.unique_bwt):
            ascii_code = self.decode_ascii()
            huffman_len = self.decode_elias()
            huffman_str = reader.read_bitstr(huffman_len)


            print(ascii_code, huffman_len, huffman_str)


    def construct_huffman_tree(self):
        pass


    # Go through constructed huffman tree and get relevant ascii character
    def decode_huffman(self):
        pass

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
        

    def decode_ascii(self):
        ascii_bits = reader.read_bitstr(ASCII_HEADER_SIZE)
        return int(ascii_bits, 2)
       
            

'''
BinaryReader class to handle the logic of reading bytes and unpacking bits.
Provides read_bit, read_bitarray, read_bits, read_bitstr methods.
'''
class BinaryReader: 

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
    - To access the bit_array, use get_bitarray method
    '''
    def read_bitarray(self):
        if self.__file is None:
            raise IOError("File needs to be open first")
        
        if 0 < self.__bitptr < BYTE_SIZE:
            return 

        file = self.__file
        byte = file.read(1)

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
    Will read and return a list of specified
    amount of bits
    '''
    def read_bits(self, count):
        bits = []
        for _ in range(count):
            bit = self.read_bit()
            if bit is not None:
                bits.append(str(bit))

        return bits
    
    
    def read_bitstr(self, count):
        bits = self.read_bits(count)
        return ''.join(bits)
    

    def get_bitarray(self):
        if self.__bitarray is None:
            return []
        return list(self.__bitarray)


    def __del__(self):
        if self.__file is not None:
            self.close_file()

        


if __name__ == "__main__":
    _, encodedfile = sys.argv

    reader = BinaryReader(encodedfile)
    decoder = Decoder(reader)
    txt = decoder.decode()

    # with open(OUTPUT_FILE, 'w') as file:
    #     file.write(txt)




