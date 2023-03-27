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
    
    bad_character_matrix(pat)

''' Bad character shifts for each position and letter of the pattern
# O(m) complexity
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
def good_suffix(pat):
    z_array = z_suffix(pat)
    m = len(pat)
    gs_array = [None]* (m + 1)

    for i in range(m-1):
        ind = m - z_array[i]
        gs_array[ind] = i
        
    return gs_array

'''Longest suffix of the good suffix that matches the prefix of the pattern'''
def matched_prefix(pat):
    pass



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
    print(bad_character_matrix("aba"))
    print(good_suffix("abab"))

    


