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
def compare_matches(str, ind):
    if ind >= len(str):
        raise ValueError("Invalid index")

    left = 0
    right = ind
    count = 0
    while str[left] == str[right]:
        count, right, left = count+1, right+1, left+1

        if right >= len(str):
            break

    return count

'''
Iterative implementation. 
O(n)
Issues:
    Move l, r computation to compare_matches
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

    if z_values[0] > 0:
        l = 1
        r = z_values[0] 

    for k in range(2, len(str)):
        if k > r:
            z_values[k-1] = compare_matches(str, k)
            
            if z_values[k-1] > 0:
                l = k
                r = k + z_values[k-1] - 1

        elif z_values[k - l-1] < r - k + 1:
            z_values[k-1] = z_values[k-l-1]
        
        else:
            z_values[k-1] = r - k + 1 + compare_matches(str, k+1)
            l = k
            r = k + z_values[k-1] + 1

    return z_values
            
    
if __name__ == "__main__":
    # naive_pattern_match('bbabaxababay', 'aba')
    print(naive_z_algorithm("ababac"))
    print(z_algorithm("ababac"))

        
                    


    
        


        