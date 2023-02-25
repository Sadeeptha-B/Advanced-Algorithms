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
        
naive_pattern_match('bbabaxababay', 'aba')

        
                    


    
        


        