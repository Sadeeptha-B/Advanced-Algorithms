import sys

OUTPUT_FILE = 'recovered.txt'

class Decoder:
    def __init__(self) -> None:
        pass

    def decode(self):
        pass

    def invert_bwt(self):
        pass


if __name__ == "__main__":
    _, encodedfile = sys.argv

    decoder = Decoder()
    txt = decoder.decode()

    with open(OUTPUT_FILE, 'w') as file:
        file.write(txt)




