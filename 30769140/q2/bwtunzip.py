import sys

OUTPUT_FILE = 'recovered.txt'
BYTE_SIZE = 8 # 1 byte is 8 bits

class Decoder:
    def __init__(self, reader):
        self.reader = reader
        self.complete = False

    def decode(self):
        reader.open_file()
        self.process_header()

        # Process data

        reader.close_file()


    def process_header(self):
        
        bytearray = reader.read_bytearray()
    

        


        # num = ord(byte)
        # pad_zeros = 8 - num.bit_length()

        # self.decode_elias((pad_zeros, num))
        
        # print(f"{ord(byte):08b}")

    def handle_bytearray(self):
        pass


    def decode_elias(self, byte_lst):
        pad_zeros, num = byte_lst
        bit_len = 1

        for i in range(pad_zeros):
            bit_len += 1


             # read next two according to bit len
             
            


class BinaryReader: 

    def __init__(self, filename):        
        if filename is None:
            raise ValueError('Filename cannot be None')

        self.__filename = filename
        self.__file = None

        
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


    def read_bytearray(self):
        if self.__file is None:
            raise IOError("File needs to be open first")

        file = self.__file
        byte = file.read(1)

        zeros, num = 0, 0

        if byte:
            num = ord(byte)
            zeros = BYTE_SIZE - num.bit_length()

        return self.__parse_byte((zeros, num))


    def __parse_byte(self, byte_lst):
        zeros, num = byte_lst
        bytearray = []

        for _ in range(zeros):
            bytearray.append('0')

        bits = num.bit_length() - 1

        for _ in range(num.bit_length()):
            start = num >> bits
            lsb = start % 2
            bytearray.append(str(lsb))
            bits -= 1

        return bytearray




        
        


if __name__ == "__main__":
    _, encodedfile = sys.argv

    reader = BinaryReader(encodedfile)
    decoder = Decoder(reader)
    txt = decoder.decode()

    # with open(OUTPUT_FILE, 'w') as file:
    #     file.write(txt)




