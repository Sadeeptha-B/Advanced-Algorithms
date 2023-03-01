'''
Align the left side of ref and pat and compare each till either pattern matches 
or does not match, either on match or not-match, compare from the next ref index
onwards, till the right side of pat is aligned with the right side of ref

-> Nested loops (One to move index after each loop, one to do the comparison for the 
particular loop)

Time complexity: O((m-n + 1)* m)

Maybe improve:
-> Maybe have auxiliary ds keep track of matched locations and then loop that sections 
only (Complexity: O(n + m* matches))
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

def naive_z_algorithm(str):
    z_array = [0]* (len(str) - 1)

    # (n-1) + (n-2) ... 2 + 1 => o(n^2)
    for i in range(1, len(str)):
        z_array[i-1] = compare_matches(str, i)

    return z_array
            
# O(n-i) => O(n)
def compare_matches(str, ind):
    left = 0
    right = ind
    count = 0
    while str[left] == str[right]:
        count, right, left = count+1, right+1, left+1

    return count

def z_algorithm(str):
    pass      
    
if __name__ == "__main__":
    # naive_pattern_match('bbabaxababay', 'aba')
    print(naive_z_algorithm("ababac"))

        
                    


    
        


        