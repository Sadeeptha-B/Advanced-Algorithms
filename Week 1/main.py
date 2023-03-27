
'''
Align the left side of ref and pat and compare each till either pattern matches 
or does not match, either on match or not-match, compare from the next ref index
onwards, till the right side of pat is aligned with the right side of ref

-> Nested loops (One to move index after each loop, one to do the comparison for the 
particular loop)

Time complexity: O((m-n + 1)* m)
'''
def naive_pattern_match(ref, pat):
    ind = 0

    while ind + len(pat) <= len(ref):
        match = True
        for i in range(len(pat)):
            if ref[ind+i] != pat[i]:
                match = False
                break
        
        if match:
            print(ind+1) # To print letter position indexed by 1
        ind += 1

'''
Perform comparison from the second element O(n^2)
'''
def naive_z_algorithm(str):
    z_array = [0]* (len(str) - 1)

    # (n-1) + (n-2) ... 2 + 1 => o(n^2)
    for i in range(1, len(str)):
        z_array[i-1] = compare_matches(str, i)

    return z_array


'''Comparison O(n-i) -> O(n)'''
def compare_matches(str, ind, left = 0):
    if ind >= len(str):
        raise ValueError("Invalid index")
    
    if left > ind:
        raise ValueError("left cannot be greater than ind")
    
    count = 0

    for right in range(ind, len(str)):
        if str[left] == str[right]:
            count += 1
            left += 1
        else:
            break

    return count

'''
Iterative implementation. 
O(n)
Issues:
    index wrangling bit too complicated, hard to debug
'''
def z_algorithm(str):
    z_values = [-1]*(len(str)-1)
    l = 0
    r = 0

    if len(str) < 2:
        return z_values

    # Base case
    z_values[0] = compare_matches(str, 1)
    l, r = update_params(z_values[0], 1, 0, 0)

    for k in range(2, len(str)):
        if k > r:
            z_values[k-1] = compare_matches(str, k)
            l, r = update_params(z_values[k-1], k, l, r)

        elif z_values[k - l-1] < r - k + 1:
            z_values[k-1] = z_values[k-l-1]
        
        else:
            z_values[k-1] = r - k + 1 + compare_matches(str, k+1, r - k + 1)
            l, r = update_params(z_values[k-1], k, l, r)

    return z_values

'''
Update left, right based on whether z_value is non zero
'''
def update_params(z_value, k, left, right):
    if z_value > 0:
        left = k
        right = z_value + k - 1

    return left, right


def z_algorithm_pattern_match(ref, pat):
    # O(m+n)
    str = pat + '$' + ref
    
    z_values = z_algorithm(str)

    for i in range(len(pat), len(z_values)):
        if z_values[i] == len(pat):
            print(i - len(pat)+1)


def is_cyclic_rotation(str1, str2):
    if len(str1) != len(str2):
        raise ValueError('str1 and str2 must be of the same length')

    st1 = f'{str1}${str2}'
    st2 = f'{str2}${str1}'

    z_values1 = z_algorithm(st1)
    z_values2 = z_algorithm(st2)

    flag = False
    ind = len(z_values1) - len(str1) + 1

    for i in range(len(z_values2) -1, len(str1) - 1, -1):
        if z_values1[ind] + z_values2[i] == len(str1):
            flag = True
            break
        ind += 1
    
    return flag



if __name__ == "__main__":
    # Z algorithm
    # print(naive_z_algorithm("ababac"))
    # print(z_algorithm("ababac"))

    # print(z_algorithm('aba$bbabaxababay'))
    # print(naive_z_algorithm('aba$bbabaxababay'))

    # # Pattern match 
    z_algorithm_pattern_match('bbabaxababay', 'aba')
    # naive_pattern_match('bbabaxababay', 'aba')

    # print(is_cyclic_rotation('abcdef', 'defabc'))
    # print(is_cyclic_rotation('isa'))
        
                    


    
        


        