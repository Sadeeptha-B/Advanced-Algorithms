import sys

OUTPUT_FILE = 'recovered.txt'
BUFFER_SIZE = 8

class Decoder:
    def __init__(self, reader):
        self.reader = reader


    def decode(self):
        reader.open_file()
        self.process_header()


    def process_header(self):
        reader.read_chunk()

    



class BinaryReader: 
    BUFFERSIZE = 8 # Bytes

    def __init__(self, filename):
        self.__buffer = b''
        
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

    
    def read_chunk(self):
        self.__buffer = self.__file.read(BUFFER_SIZE)
        


if __name__ == "__main__":
    _, encodedfile = sys.argv

    reader = BinaryReader(encodedfile)
    decoder = Decoder(reader)
    txt = decoder.decode()

    # with open(OUTPUT_FILE, 'w') as file:
    #     file.write(txt)




