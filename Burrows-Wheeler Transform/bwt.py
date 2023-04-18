ALPHABET_SIZE = 27

'''
Quick and dirty suffix array construction runs in O(n* sorting * comparison cost)
Inbuilt python sort runs in O(nlogn)
O(n) space
'''
def get_suffix_array(st):
    arr = list(range(0, len(st)))

    # Built in sort, with string slicing
    arr.sort(key=lambda x: st[x::])
    return arr


'''
Gets BWT string from provided suffix array and string.
The string should have the $ character appendended
O(n) time and space
'''
def get_bwt(suffix_array, st):
    res = []
    n = len(suffix_array)

    # Loop over suffix array, get cyclic index after -1 and corresponding character
    for elem in suffix_array:
        ind = (elem - 1) % n
        res.append(st[ind])

    return ''.join(res)

'''
Inverts the BWT string in O(n) time
Uses LF mapping
'''
def invert_bwt(bwt):
    n = len(bwt) - 1
    res = [None] * n 

    rank, occ = compute_rank_occ(bwt) # O(n)

    i = n - 1
    next_i = 0
    char = bwt[next_i]

    '''
    Constructs the results array one by one by going back through the string
    '''
    while char != "$":
        res[i] = char
        next_i = rank[ord(char) - 97 + 1] + occ[next_i]
        char = bwt[next_i]
        i -= 1
    
    return ''.join(res)
        
        
'''
From a given BWT string, computes the rank of each character in the string, as per the suffix array
positions as well as the number of occurences of each character thus far, at each index.
'''
def compute_rank_occ(bwt):
    arr = [None]*ALPHABET_SIZE
    occ = [None]* len(bwt)

    # Calculate the count of each character occurence
    for i, char in enumerate(bwt):
        if char == "$":
            arr[0] = 1
            occ[i] = 0
            continue

        ind = ord(char) - 97 + 1
        
        if arr[ind] is None:
            arr[ind] = 1
            occ[i] = 0
        else:
            occ[i] = arr[ind]
            arr[ind] += 1
    

    # Maintain a running count to keep track of rank
    run_count = 0
    for i in range(len(arr)):

        if arr[i] is not None:
            value = arr[i]
            arr[i] = run_count
            run_count += value
            
    return arr, occ
    

if __name__ == "__main__":
    # Preprocessing string input
    # Adding a unique character in order to ensure full ordering
    st = "googol" + "$"

    # Get suffix array
    suffix_array = get_suffix_array(st)

    # get bwt string
    bwt = get_bwt(suffix_array, st)

    # Invert bwt to retrieve string
    retrieved_st = invert_bwt(bwt)

    print(suffix_array)
    print(bwt)
    print(retrieved_st)
