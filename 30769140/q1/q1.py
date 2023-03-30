'''
Author: Sadeeptha Bandara
Student ID: 30769140

'''
import sys

OUTPUT_FILE = "output_q1.txt"
PREFIX = 0
SUFFIX = 1


def pattern_match_transpose(ref, pat):
    z_array = z_prefix_suffix(ref, pat) 

    n = len(ref)
    m = len(pat)
    i = 0
    res = []
    transpose = []

    while i + m <= n:
        
        # Considering alignment
        front = z_array[i][PREFIX]
        back =  z_array[i + m -1][SUFFIX]

        if front == m:
            res.append(i+1)
            i += 1
            continue
        
        
        gap = m - (front + back)
        
        if gap == 2:   
            is_transposition = ref[i + front] == pat[front+1] and pat[front] == ref[i+front+1]

            if is_transposition:
                transpose.append((i+1, i+front+1))

        i+= 1
            
    return res, transpose

'''
Z algorithm implemented for both prefix and suffix. Primarily to reduce the complexity cost of 
looping twice to compute z_prefix and z_suffix separately.
'''
def z_prefix_suffix(ref, pat):
    n = len(ref)
    z_array = [[None, None] for _ in range(n)]

    if n == 0:
        return z_array
    
    z_pat = z_base(pat)
    z_suffix_pat = z_suffix_base(pat)

    # Right and left pointers for prefix and suffix z boxes
    r_p, l_p = -1,-1
    r_s, l_s = n, n

    for i_p in range(0, n):

        # Suffix index
        i_s = n - 1 - i_p

        # Computing z value and mutating r and l
        z_array[i_p][PREFIX], r_p, l_p = z_i(ref, pat, z_pat, r_p, l_p, i_p)
        z_array[i_s][SUFFIX], r_s, l_s = z_suffix_i(ref, pat, z_suffix_pat, r_s, l_s, i_s)


    return z_array


'''
Compute the z_prefix value at a particular index provided the r, l and z_array
'''
def z_i(ref, pat, z_pat, r, l, i):
    in_box = i <= r

    if in_box:
        
        ind = i - l   # Corresponding index to i 
        rem = r - i + 1   # Matching region as per lr box
        z_ind = z_pat[ind]

        if z_ind < rem:
            z_value = z_ind

        elif z_ind > rem:
            z_value = rem
            
        else:
            z_value = rem + compare_matches(ref, pat, r-i+1, r+1)
            r = i + z_value - 1
            l = i

    else:
        z_value = compare_matches(ref, pat, 0, i)     
        r = i + z_value - 1
        l = i

    return z_value, r, l


'''
Compute the z_suffix value at a particular index provided the r,l and z_array
'''
def z_suffix_i(ref, pat, z_pat, r, l, i):
    m  = len(pat)

    in_box = l <= i

    if in_box:
        ind = m - (r-i) - 1
        rem = i - l + 1
        z_ind = z_pat[ind]

        if z_ind < rem:
            z_value = z_ind

        elif z_ind > rem:
            z_value = rem

        else:
            z_value = rem + compare_matches_invert(ref, pat, (m-1) - (i-l+1), l-1)
            l = i - z_value + 1
            r = i

    else:
        z_value = compare_matches_invert(ref, pat, m-1, i)
        l = i - z_value + 1
        r = i
    return z_value, r, l

# Basic z algo implementations for a provided string
# ====================================================================================================

def z_base(st):
    z_array = [None] * len(st)

    if len(st) == 0:
        return z_array

    z_array[0] = len(st)
    r, l = 0, 0

    for i in range(1, len(st)):
        in_box = i <= r

        if in_box:
            ind = i - l
            rem = r - i + 1

            if z_array[ind] < rem:
                z_array[i] = z_array[ind]

            elif z_array[ind] > rem:
                z_array[i] = rem
                
            else:
                z_array[i] = rem + compare_matches(st, st,  r-i+1, r+1)
                r = i + z_array[i] - 1
                l = i

        else:
            z_array[i] = compare_matches(st, st, 0, i)     
            r = i + z_array[i] - 1
            l = i
    
    return z_array
    

def z_suffix_base(st):
    n = len(st)
    z_array = [None] * n

    if n == 0:
        return z_array
    
    z_array[-1] = n
    l, r = n - 1, n - 1

    for i in range(len(st)-2, -1, -1):
        in_box = l <= i

        if in_box:
            ind = n - (r-i) - 1
            rem = i - l + 1

            if z_array[ind] < rem:
                z_array[i] = z_array[ind]

            elif z_array[ind] > rem:
                z_array[i] = rem

            else:
                z_array[i] = rem + compare_matches_invert(st, st, (n-1) - (i-l) -1, l-1)
                l = i - z_array[i] + 1
                r = i

        else:
            z_array[i] = compare_matches_invert(st, st, n-1, i)
            l = i - z_array[i] + 1
            r = i

    return z_array




# Helper functions
# =========================================================================================================

# def compare_matches(st, start, end):
#     count = 0

#     while end < len(st) and st[start] == st[end]:
#         count += 1
#         start += 1
#         end+= 1

#     return count


# def compare_matches_invert(st, start, end):
    count = 0

    while start >= 0  and st[start] == st[end]:
        count += 1
        start -= 1
        end -= 1

    return count


# Helper functions
#=====================================================================================================
def compare_matches(ref, pat, start , i):
    count = 0

    while start < len(pat) and i < len(ref):
        if ref[i] != pat[start]:
            break

        count += 1
        start += 1
        i+= 1
    
    return count

def compare_matches_invert(ref, pat, start, i):
    count = 0

    while start >= 0 and i >= 0:
        if pat[start] != ref[i]:
            break
        count += 1
        start -= 1
        i -= 1

    return count



# I/O operations
# =========================================================================================================

def open_file(filename):
    st = ""

    with open(filename, 'r') as file:
        for line in file:
            st += line.stip()

    return st

def write_output(output):
    with open(OUTPUT_FILE, 'a') as file:
        file.write(f"\n{output}")
    

def z_prefix(ref, pat, z_pat):
    n = len(ref)

    z_array = [None]*n

    if n == 0:
        return z_array
    
    r,l = -1, -1

    for i in range(0, n):
        in_box = i <= r

        if in_box:
            ind = i - l
            rem = r - i + 1
            z_ind = z_pat[ind]

            if z_ind < rem:
                z_array[i] = z_ind

            elif z_ind > rem:
                z_array[i] = rem 
                
                
            else:
                z_array[i] = rem + compare_matches(ref, pat, r-i+1, r+1)
                r = i + z_array[i] - 1
                l = i

        else:
            z_array[i] = compare_matches(ref, pat, 0, i)
            r = i + z_array[i] - 1
            l = i
        # print(i)

    return z_array


def z_suffix(ref, pat, z_pat):
    n = len(ref)
    m = len(pat)

    z_array = [None]* n

    if n == 0:
        return z_array
    
    r, l = n, n

    for i in range(n-1, -1, -1):
        in_box = l <= i

        if in_box:
            ind = m - (r-i) - 1
            rem = i - l + 1
            z_ind = z_pat[ind]

            if z_ind < rem:
                 z_array[i] = z_ind

            elif z_ind > rem:
                z_array[i] = rem

            else:
                print(i)
                z_array[i] = rem + compare_matches_invert(ref, pat,  (m-1) - (i-l+1), l-1)
                l = i - z_array[i] + 1
                r = i

        else:
            z_array[i] = compare_matches_invert(ref, pat, m - 1, i)
            l = i - z_array[i] + 1
            r = i

    return z_array







if __name__ == "__main__":
    # _, filename1, filename2 = sys.argv

    # text = open_file(filename1)
    # pattern = open_file(filename2)

    # q1_solution(text, pattern)    

    print(pattern_match_transpose("babbababaabbaba", "abba"))
    # print(z_prefix_suffix("abba$babbababaabbaba$abba"))
    # print(z_prefix("babbababaabbaba", "abba"))
    # z_pat = z_base("abba")
    # print(z_pat)
    # print(z_prefix("babbababaabbaba", "abba", z_pat))
    # print(z_suffix("babbababaabbaba", "abba", [1,0, 0, 4]))
    # print(z_prefix_suffix("babbababaabbaba", "abba"))