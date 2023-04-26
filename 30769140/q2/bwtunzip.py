import sys
import warnings

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
       
            


class BinaryReader: 

    def __init__(self, filename):        
        if filename is None:
            raise ValueError('Filename cannot be None')

        self.__filename = filename
        self.__file = None
        self.__bitptr = 0
        self.__bitarray = None

        
    def set_file(self, filename):
        if self.__file is not None:
            raise IOError('Close currently opened file')
        
        if filename is None:
            raise TypeError('Filename cannot be None')

        self.__filename = filename


    def open_file(self, filename=None):
        if self.__file is not None:
            raise IOError('Close currently opened file')
        
        if filename is not None:
            self.set_file(filename)

        self.__file = open(self.__filename, 'rb')

    def close_file(self):
        if self.__file is not None:
            self.__file.close()

        self.__file = None


    def __read_bitarray(self):
        if self.__file is None:
            raise IOError("File needs to be open first")

        file = self.__file
        byte = file.read(1)

        zeros, num = 0, 0

        if byte:
            num = ord(byte)
            zeros = BYTE_SIZE - num.bit_length()

        self.__bitarray = self.__parse_byte((zeros, num)) 
        self.__bitptr = 0


    def __parse_byte(self, byte_lst):
        zeros, num = byte_lst
        bitarray = []

        for _ in range(zeros):
            bitarray.append(0)

        bits = num.bit_length() - 1

        for _ in range(num.bit_length()):
            start = num >> bits
            lsb = start % 2
            bitarray.append(lsb)
            bits -= 1

        return bitarray


    def read_bit(self):
        if self.__bitarray is None:
            self.__read_bitarray()

        if self.__bitptr >= BYTE_SIZE:
            raise RuntimeError('Pointer cannot exceed bitarray bounds')

        if len(self.__bitarray) == 0:
            return None
        
        bit = self.__bitarray[self.__bitptr]
        self.__bitptr += 1

        if self.__bitptr >= BYTE_SIZE:
            self.__read_bitarray()

        return bit
    

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




