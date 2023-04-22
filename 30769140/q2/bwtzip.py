'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = "bwtencoded.bin"

def naive_suffix_array(text):
    arr = list(range(len(text))) #O(n)
    arr.sort(key = lambda x: text[x::]) # O(n* nlogn * comparison)

    return arr

def get_bwt(text):
    suffix_array = naive_suffix_array(text)
    n = len(suffix_array)
    res = []

    # Loop over suffix array, get cyclic index after -1 and corresponding character
    for elem in suffix_array:
        ind = (elem - 1) % n
        res.append(text[ind])

    return ''.join(res)


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

    # Append terminal character
    text += "$"

    bwt = get_bwt(text)
    print(bwt)


