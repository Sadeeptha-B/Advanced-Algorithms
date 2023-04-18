'''
Quick and dirty suffix array construction 
runs in O(n^2 logn * comparison cost)
'''
def suffix_array(st):
    st += "$" # Unique character 
    arr = list(range(0, len(st)))

    # Built in sort, with string slicing
    arr.sort(key=lambda x: st[x::])
    return arr

def bwt(suffix_array):
    res = []
    n = len(suffix_array)

    for elem in suffix_array:
        res.append((elem - 1) % n )
    
    return res

if __name__ == "__main__":
    a = suffix_array("googol")
    b = bwt(a)
    print(a)
    print(b)
