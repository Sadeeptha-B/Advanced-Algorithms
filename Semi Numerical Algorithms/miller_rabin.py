'''
Performs the fermat test of the form
        do a^(n-1) and 1 belong to the same congruence class of modulo n ?
multiple times in performing the miller rabin test

num :- Number to test primality
tests : Amount of fermat tests to perform

Makes use of modular exponentiation to terminate a chosen test early/ to reduce
fermat's liar cases.
'''
def miller_rabin_primality(num, tests):    
    if num == 1:
        raise ValueError('1 is neither prime nor composite')

    # Special cases
    if num == 2 or num == 3:
        return True
    
    # All even numbers except two are non-prime
    if num % 2 == 0:
        return False
    
    # Converting to a form suitable for mod exp
    # Finding s and t such that num - 1 = 2^s * t
    s, t = 0, num - 1

    while t % 2 == 0:
        s = s + 1
        t = t / 2
    
    t = int(t)

    # Perform fermat's test multiple times
    for _ in range(tests):
        
        a = random.randint(2, num-2)
        previous = num -1
        current = (a ** t) % num   # Mod exp starting term

        for _ in range(s+1):

            # Check for first occurence of mod exp becoming 1
            if current == 1:
                if previous != num-1:
                    return False
                else:
                    break

            previous = current
            current = (current ** 2) % num   # Repeated squaring

    return True