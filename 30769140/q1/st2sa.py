'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''
import sys

OUTPUT_FILE = "output_sa.txt"

class Ukkonen:
    def __init__(self) -> None:
        pass

# I/O operations
# ==================================================================================================

def open_file(filename):
    st = ""

    with open(filename, 'r') as file:
        for line in file:
            st += line.strip()

    return st

'''
Takes in a zero-indexed suffix array and writes to output file in 1-indexed form
'''
def write_output(suffix_array):
    with open(OUTPUT_FILE, 'w') as file:
        for ind in suffix_array:
            file.write(f"{ind+1}\n")

if __name__ == "__main__":
    _, inputfile = sys.argv

    # It is assumed that there are no line breaks in the input file
    # All characters are within the ascii range [37, 126]
    text = open_file(inputfile)

    # Append terminal character
    text += "$"

    # Construct suffix tree using Ukkonen class

    # Create suffix array from suffix tree: Inorder traversal

    # Write output to file
