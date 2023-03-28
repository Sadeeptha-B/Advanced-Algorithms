def kmp(ref, pat):
    pass

def sp_i(pat):
    m = len(pat)
    sp_array = [None]* m




    pass



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
    pass