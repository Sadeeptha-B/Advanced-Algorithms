'''
Author: Sadeeptha Bandara
Student ID: 30769140

'''


import sys

OUTPUT_FILE = "output_q2.txt"
ALPHABET_SIZE = 26
WILDCARD_DIFF = 46 - 97
WILDCARD = "."

'''
A standard boyer moore implementation.

'''
def boyer_moore(ref, pat):

    # Pre-processing
    bc_matrix = bc_matrix_wc(pat)  # O(26m)
    wc_ind, z_array = z_suffix_wc(pat)
    
    gs_array, mp_array = gs_mp(z_array)
    res = []

    n = len(ref)
    m = len(pat)
    current = 0

    # Align left to right
    while current + m <= n:
        i = m-1
        stop, start = m, m
        
        # Right to left scanning
        while i >= 0 and (i < start or i> stop):
            
            r_ind = current + i 
            p_ind = i

            # If mismatch
            if ref[r_ind] != pat[p_ind]:
                char = bc_matrix[ord(ref[r_ind]) - 97]

                bc = char[p_ind] if char is not None else -1     
                gs = gs_array[p_ind + 1]

                # bad character shift
                bc_shift = p_ind - bc
                 
                # Good suffix and match prefix condition
                if gs is not None:
                    gs_shift = m -1 - gs
                    stop, start = gs, gs - z_array[gs] + 1
                else:
                    gs_shift = m - 1 - mp_array[i+1]
                    stop, start = mp_array[i], 0

                # Perform optimal shift
                shift = max(bc_shift, gs_shift)
                current += shift 
                break
            
            # Match occurence
            if i == 0:
                res.append(current)
                shift = m - 1 - mp_array[1]
                stop, start = mp_array[1], 0
                current += shift
            
            i -= 1
        
    return res



'''To compute good suffix and matched prefix both'''
def gs_mp(z_array):
    m = len(z_array)
    gs_array = [None]*(m+1)
    mp_array = [-1]*(m+1)
    m_ind = None

    for i in range(m-1):
        p_ind = m - z_array[i]
        gs_array[p_ind] = i

        if i == z_array[i] - 1:
            m_ind = p_ind
            mp_array[m_ind] = i
        elif m_ind is not None:
            m_ind -= 1
            mp_array[m_ind] = mp_array[m_ind+1]

    return gs_array, mp_array


''' 
Bad character shifts for each position and letter of the pattern
O(m) complexity
'''
def bc_matrix_wc(pat):
    mat = [None] * ALPHABET_SIZE # O(26)

    #O(26m)
    for pat_i in range(len(pat)-1, -1, -1):
        ind = ord(pat[pat_i]) - 97

        if ind == WILDCARD_DIFF:
            for i in range(len(mat)):
                fill_bc_row(mat, pat, i, pat_i)
            continue

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


'''Longest substring ending at each index that matches the suffix of the input string'''
def z_suffix_wc(st):
    n = len(st)
    z_array = [None] * n

    if n == 0:
        return z_array
    
    z_array[-1] = n
    l, r = n - 1, n - 1

    # Wildcard index
    wc_ind = find_wc_ind(st)

    for i in range(len(st)-2, -1, -1):
        in_box = l <= i


        if in_box:
            ind = n - (r-i) - 1
            rem = i - l + 1
            z_ind = z_array[ind]

            # If wildcard is at index ind
            if ind == wc_ind:
                if st[i] != st[-1]:
                    z_array[i] = 0
                    continue
                
            # Check if wildcard is in matched region
            wc_gap = ind - wc_ind + 1
            wc_in_rem = wc_gap <= rem


            if z_ind < rem:
                z_array[i] = z_ind

                # If wildcard is at index i
                if z_ind == 0 and i==wc_ind:
                    z_array[i] = compare_matches_invert_wc(st, n-1, i)
                    
                    if z_array[i] > rem:
                        l = i - z_array[i] + 1
                        r = i
                    continue
                    
                # If wild card is in the remaining region
                if wc_in_rem:
                    if wc_gap == z_ind and wc_gap != 0:
                        z_array[i] = wc_gap if st[n - wc_gap] == st[i - wc_gap + 1] else wc_gap -1
                    elif wc_gap < z_ind and wc_gap != 0:
                        z_array[i] = z_ind if st[n - wc_gap] == st[i - wc_gap + 1] else wc_gap -1
                    
            
            elif z_ind > rem:
                z_array[i] = rem

                if wc_in_rem:
                    if  wc_gap > 0 and st[n - wc_gap] != st[i - wc_gap + 1]:
                        z_array[i] = wc_gap -1


            else:
                if wc_in_rem:
                    if st[n-wc_gap] != st[i - wc_gap + 1]:
                        z_array[i] = wc_gap -1

                z_array[i] = rem + compare_matches_invert_wc(st, (n-1) - (i-l) -1, l-1)
                l = i - z_array[i] + 1
                r = i

        else:
            z_array[i] = compare_matches_invert_wc(st, n-1, i)
            l = i - z_array[i] + 1
            r = i

    return wc_ind, z_array


def compare_matches_invert_wc(str, end, start):
    count = 0

    while start >= 0:
        if str[start] != str[end]:
            cond = str[start] == '.' or str[end] == '.'

            if not cond:
                break
        
        count += 1
        start -= 1
        end -= 1

    return count


'''
Returns index of wildcard in provided string, returns -1 if not found
'''
def find_wc_ind(st):
    for i, letter in enumerate(st):
        if letter == WILDCARD:
            return i
    
    return -1



# I/O 
# ======================================================================================
def open_file(filename):
    str = ""

    with open(filename, 'r') as file:
        for line in file:
            str += line.strip()

    return str


def write_output(results):
    with open(OUTPUT_FILE, 'w') as file:
        for res in results:
            file.write(f"{res}\n")
        

if __name__ == "__main__":
    _, filename1, filename2 = sys.argv

    text = open_file(filename1)
    pattern = open_file(filename2)


    write_output(boyer_moore(text, pattern))
    



