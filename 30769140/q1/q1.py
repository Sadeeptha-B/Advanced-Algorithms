'''
Author: Sadeeptha Bandara
Student ID: 30769140

'''
import sys

OUTPUT_FILE = "output_q1.txt"
PREFIX = 0
SUFFIX = 1


def pattern_match_transpose(ref, pat):
    z_array = z_prefix_suffix(ref)



'''
Z algorithm implemented for both prefix and suffix. Primarily to reduce the complexity cost of 
looping twice to compute z_prefix and suffix separately.
'''
def z_prefix_suffix(st):
    n = len(st)
    z_array = [[None, None] for _ in range(n)]

    if n == 0:
        return z_array
    
    z_array[0][PREFIX] = n
    z_array[-1][SUFFIX] = n 

    # Right and left pointers for prefix and suffix z boxes
    r_p, l_p = 0,0
    r_s, l_s = n-1, n-1

    for i_p in range(1, n):

        # Suffix index
        i_s = n - 1 - i_p

        # Computing z value and mutating r and l
        z_array[i_p][PREFIX], r_p, l_p = z_i(st, z_array, r_p, l_p, i_p)
        z_array[i_s][SUFFIX], r_s, l_s = z_suffix_i(st, z_array, r_s, l_s, i_s)


    return z_array

'''
Compute the z_prefix value at a particular index provided the r, l and z_array
'''
def z_i(st, z_array, r, l, i):
    in_box = i <= r

    if in_box:
        
        ind = i - l   # Corresponding index to i 
        rem = r - i + 1   # Matching region as per lr box
        z_ind = z_array[ind][PREFIX]

        if z_ind < rem:
            z_value = z_ind

        elif z_ind > rem:
            z_value = rem
            
        else:
            z_value = rem + compare_matches(st, r-i+1, r+1)
            r = i + z_value - 1
            l = i

    else:
        z_value = compare_matches(st, 0, i)     
        r = i + z_value - 1
        l = i

    return z_value, r, l


'''
Compute the z_suffix value at a particular index provided the r,l and z_array
'''
def z_suffix_i(st, z_array, r, l, i):
    n  = len(st)
    in_box = l <= i

    if in_box:
        ind = n - (r-i) - 1
        rem = i - l + 1
        z_ind = z_array[ind][SUFFIX]

        if z_ind < rem:
            z_value = z_ind

        elif z_ind > rem:
            z_value = rem

        else:
            z_value = rem + compare_matches_invert(st, (n-1) - (i-l) -1, l-1)
            l = i - z_value + 1
            r = i

    else:
        z_value = compare_matches_invert(st, i, n-1)
        l = i - z_value + 1
        r = i
    return z_value, r, l
    



# Helper functions
# =========================================================================================================

def compare_matches(st, start, end):
    count = 0

    while end < len(st) and st[start] == st[end]:
        count += 1
        start += 1
        end+= 1

    return count


def compare_matches_invert(st, start, end):
    count = 0

    while start >= 0  and st[start] == st[end]:
        count += 1
        start -= 1
        end -= 1

    return count




'''
I/O Operations
'''
def open_file(filename):
    st = ""

    with open(filename, 'r') as file:
        for line in file:
            st += line.stip()

    return st

def write_output(output):
    with open(OUTPUT_FILE, 'a') as file:
        file.write(f"\n{output}")
    

if __name__ == "__main__":
    # _, filename1, filename2 = sys.argv

    # text = open_file(filename1)
    # pattern = open_file(filename2)

    # q1_solution(text, pattern)    
    print(z_prefix_suffix(""))

    # same char
    print(z_prefix_suffix("aaaaaa"))

    # different char
    print(z_prefix_suffix("abcdefg"))

    # case 2a: z_(i_p-l) < rem
    print(z_prefix_suffix("abacabacc"))

    # case 2b: z_(i_p-l) > rem
    print(z_prefix_suffix("abacababa"))

    # case 2c: z_(i_p-l) = rem
    print(z_prefix_suffix("ababac"))
    