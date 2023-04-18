ALPHABET_SIZE = 27

'''
Quick and dirty suffix array construction 
runs in O(n^2 logn * comparison cost)
'''
def get_suffix_array(st):
    arr = list(range(0, len(st)))

    # Built in sort, with string slicing
    arr.sort(key=lambda x: st[x::])
    return arr

'''
Gets BWT string from provided suffix array and string.
The string should have the $ character appendended
'''
def get_bwt(suffix_array, st):
    res = []
    n = len(suffix_array)

    for elem in suffix_array:
        ind = (elem - 1) % n
        res.append(st[ind])

    return ''.join(res)


def invert_bwt(bwt):
    res = [None] * (len(bwt) - 1)
    pass


def compute_rank_occ(bwt):
    arr = [None]*ALPHABET_SIZE
    occ = [None]* len(bwt)

    
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
    
    run_count = 1
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

    print(suffix_array)
    print(bwt)
    print(compute_rank_occ(bwt))
