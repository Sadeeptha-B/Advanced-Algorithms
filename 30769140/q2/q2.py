'''
Author: Sadeeptha Bandara
Student ID: 30769140

'''

'''
Assignment 2 briefing summary

- q2 briefing from 49:00
- bad character array shouldn't be too different
- preprocessing to get optimal shift accounting for 
    wildcard might not be worth it
- So don't overcomplicate the preprocessing
- consider different regions that the wildcard may be found in
- related with q1, specifically in that wildcard may be in 
different regions of the pattern


'''

import sys

OUTPUT_FILE = "output_q2.txt"
ALPHABET_SIZE = 26
WILDCARD_DIFF = 46 - 97

            
''' 
Bad character shifts for each position and letter of the pattern
O(m) complexity
'''
def bad_character_matrix(pat):
    mat = [None] * ALPHABET_SIZE # O(26)

    #O(26m)
    for pat_i in range(len(pat)-1, -1, -1):
        ind = ord(pat[pat_i]) - 97

        if ind == WILDCARD_DIFF:
            for i in range(len(mat)):
                fill_bc_row(mat, pat, i, pat_i)
            break

        fill_bc_row(mat, pat, ind, pat_i)

    return mat



def fill_bc_row(mat, pat, mat_i, pat_i):
    if mat[mat_i] is None:
        mat[mat_i] = [-1]* len(pat)

    for j in range(pat_i, len(pat)):
        if mat[mat_i][j] == - 1:
            mat[mat_i][j] = pat_i
        else:
            break







def q2_solution(ref, pat):
    pass



# I/O 
# ======================================================================================
def open_file(filename):
    str = ""

    with open(filename, 'r') as file:
        for line in file:
            str += line.strip()

    return str


def write_output(output):
    with open(OUTPUT_FILE, 'a') as file:
        file.write(f"\n{output}")
        

if __name__ == "__main__":
    # _, filename1, filename2 = sys.argv

    # text = open_file(filename1)
    # pattern = open_file(filename2)

    # q2_solution(text, pattern)    
    print(bad_character_matrix('bab.ba'))
    



