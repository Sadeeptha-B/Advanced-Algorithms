'''
Author: Sadeeptha Bandara

Knuth-Morris-Pratt algorithm

- Performs comparisons each iteration
- Within the matched region, shifts according to the 
longest proper suffix of prefix pat[1..i] where i+1 is point
of mismatch


- O(n+m) algorithm: performs comparison for each index only
once

'''

def kmp(ref, pat):
    sp_array = sp_i(pat)
    res = []

    n = len(ref)
    m = len(pat)
    current = 0
    start = 0

    # Aligning pattern to reference
    while current + m <= n:

        p_ind = start

        # Comparing left to right within an alignment
        while p_ind < m:
            
            r_ind = current + p_ind 

            # First mismatch
            if ref[r_ind] != pat[p_ind]:
                shift = p_ind - sp_array[p_ind]
                break

            p_ind += 1

        # If a match is found
        if p_ind == m:
            res.append(current)
            shift = m - sp_array[m] 

        # Optimization to avoid re-comparing matching regions
        start = sp_array[p_ind] if sp_array[p_ind] > 0 else 0
        current += shift

    return res

'''
SP[i] array:
Computes for each pat[0..i] the longest proper suffix that matches the prefix 
Returns: A list of len(pat) +1. First index will correspond to the pat[0..-1] case
other indices for each prefix of the string
'''
def sp_i(pat):
    m = len(pat)
    sp_array = [0]* (m+1)
    sp_array[0] = -1

    z_array = z_algo(pat)
    
    for j in range(m-1, 0, -1):
        i = j + z_array[j] - 1
        sp_array[i+1] = z_array[j]

    return sp_array


'''Longest substring that matches the prefix at each index of the input string'''
def z_algo(str):
    z_array = [None] * len(str)

    if len(str) == 0:
        return z_array

    z_array[0] = len(str)
    r, l = 0, 0

    for i in range(1, len(str)):
        in_box = i <= r

        if in_box:
            ind = i - l
            rem = r - i + 1

            if z_array[ind] < rem:
                z_array[i] = z_array[ind]

            elif z_array[ind] > rem:
                z_array[i] = rem
                
            else:
                z_array[i] = rem + compare_matches(str, r-i+1, r+1)
                r = i + z_array[i] - 1
                l = i

        else:
            z_array[i] = compare_matches(str, 0, i)     
            r = i + z_array[i] - 1
            l = i
    
    return z_array


def compare_matches(str, start, end):
    count = 0

    # Note that the order of the and operation is important to
    # avoid an index error
    while end < len(str) and str[start] == str[end]:
        count += 1
        start += 1
        end += 1
    
    return count


if __name__ == "__main__":
    print(sp_i("aba"))
    print(kmp('bbabaxababay', 'aba'))
