'''
Author: Sadeeptha Bandara
Credits to Raymond D'Souza for testcases and the testfile
'''

ALPHABET_SIZE = 26

'''
Boyer moore's algorithm for exact pattern matching
 - Allows you to skip unnecessary alignments in the text
 - Bad character rule: Larger skips
    Bad block optimization for small alphabets
    Creating bad character matrix

 - Good suffix rule, matched prefix rule: less comparisons
 - Galil's optimization
 - O(n/m) sublinear time

'''
def boyer_moore(ref, pat):
    
    # Pre-processing
    bc_matrix = bad_character_matrix(pat)  # O(26m)
    z_array = z_suffix(pat)
    gs_array, mp_array = gs_mp(z_array, pat)
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

            
''' 
Bad character shifts for each position and letter of the pattern
O(m) complexity
'''
def bad_character_matrix(pat):
    mat = [None] * ALPHABET_SIZE # O(26)

    #O(26m)
    for i in range(len(pat)-1, -1, -1):
        ind = ord(pat[i]) - 97

        if mat[ind] is None:
            mat[ind] = [-1]* len(pat)

        for j in range(i, len(pat)):
            if mat[ind][j] == -1:
                mat[ind][j] = i
            else:
                break
    return mat

'''
For each suffix of the pattern, the index of the rightmost occurence of itself 
within the pattern such that the previous letter mismatches
'''
def good_suffix(z_array, pat):
    m = len(pat)
    gs_array = [None]* (m + 1)

    for i in range(m-1):
        ind = m - z_array[i]
        gs_array[ind] = i
        
    return gs_array


'''Longest suffix of the good suffix "that matches the prefix of the pattern'''
def matched_prefix(z_array, pat):
    m = len(pat)
    mp_array = [m]*(m+1)
    ind = None

    for i in range(m):
        if i == z_array[i]-1:
            ind = m - z_array[i]
            mp_array[ind] = i
        elif ind is not None:
            ind -= 1
            mp_array[ind] = mp_array[ind+1]

    return mp_array


'''To compute good suffix and matched prefix both'''
def gs_mp(z_array, pat):
    m = len(pat)
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


'''Longest substring ending at each index that matches the suffix of the input string'''
def z_suffix(str):
    n = len(str)
    z_array = [None] * n

    if n == 0:
        return z_array
    
    z_array[-1] = n
    l, r = n - 1, n - 1

    for i in range(len(str)-2, -1, -1):
        in_box = l <= i

        if in_box:
            ind = n - (r-i) - 1
            rem = i - l + 1

            if z_array[ind] < rem:
                z_array[i] = z_array[ind]

            elif z_array[ind] > rem:
                z_array[i] = rem

            else:
                z_array[i] = rem + compare_matches_invert(str, (n-1) - (i-l) -1, l-1)
                l = i - z_array[i] + 1
                r = i

        else:
            z_array[i] = compare_matches_invert(str, n-1, i)
            l = i - z_array[i] + 1
            r = i

    return z_array


def compare_matches_invert(str, end, start):
    count = 0

    while start >= 0 and str[start] == str[end]:
        count += 1
        start -= 1
        end -= 1

    return count


if __name__ == "__main__":
    # print(bad_character_matrix("acababacaba"))
    # # print(good_suffix(z_suffix("abab"), "abab"))
    # z_array = z_suffix("acababacaba")
    # print(z_array)
    # # print(good_suffix(z_array, "acababacaba"))
    # # print(matched_prefix(z_array, "acababacaba"))
    # print(gs_mp(z_array, "acababacaba"))
    # print(gs_mp(z_suffix("abab"), "abab"))

    print(boyer_moore('aagacacataaagaagctttataacgtcaaggtcgcaaggcactacctattgctccccgacggttaaggttagcagctccactcccgcggaataggtacgaattatgagtgactgatttttctggtacccgggcaagagcctaaactgagcgaaacattttcattcctggctgaagatgttcatagcgtccacctcggttggccgttattccagcactggagaacaccggtcaaccaattggccactgtgcacgcgtcgttcggctgtggaagcggcggaactgacgaatagtttacctggctgtactgaacgtacacccgtctgccgttgttgttaatccattgtgccaatttagctcaccgagtcacgcgacactctgggcttgagaggcgggcgagtggttcacatggcgcggagtgtagtttgtgagatattctaggaagaacgtcgttgctaggtcacggcacagatacaggatccatacaatagttagctagcctggatggacttattctcatattgcttgtgagcagcctttaaagtggggtctacagaagtcagtaggcttatgtcgcggaaccggggccacgcgagatctaatacggttgcgaagggcgtcttatcagcgggatactgagccaatggcagtgataattccgtaggttctataagtcgggtatcagcgaccgcctagccatacccgaaatgtcggcattcctcggcaacgaacgaccatgaaccgctaagaagcgacgagccgaatcagatccggacaccgcgacccctcaactccgggctttctgagcatgaagcgtgctacatcgattttgaagtgaaagatactgggtggcgccgagtatgagtaggaggaccacatggagctttgaagatggtatttaaccccggggttatggacctcctaccggccttccgggttcgtagtcgaaggttgtccatacaggtttcgtttttgtcaaccgagcccggcaagcagtacga',
                       'ctc'))
    

    


