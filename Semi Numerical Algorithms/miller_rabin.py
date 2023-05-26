import random
from math import log
from mod_exp import mod_exp


'''
Performs the fermat test of the form
        do a^(n-1) and 1 belong to the same congruence class of modulo n ?
multiple times in performing the miller rabin test
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
    print(f"s: {s}, t: {t}")

    # Perform fermat's test multiple times
    for i in range(tests):
        a = random.randint(2, num-2)
        print(f"Test {i+1}, a={a} :")
        
        previous = num -1
        current = mod_exp(a, t, num)  # Mod exp starting term

        for _ in range(s):
            print(current)
            # Check for first occurence of mod exp becoming 1
            if current == 1:
                if previous != num-1:
                    return False
                else:
                    break

            previous = current
            current = (current ** 2) % num   # Repeated squaring
        print('---------')

        if current != 1 or (current == 1 and previous != num-1):
            return False

    return True



if __name__ == "__main__":
    num = 1023
    confidence = int(log(num) + 1)
    print("Miller rabin test")
    print(num, confidence)
    print("===================")

    print(miller_rabin_primality(num, confidence))

    # Carmichael numbers
    # nums = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461, 252601, 278545, 294409, 314821, 334153]
    # for num in nums:
    #     tests = int(log(num)) + 1
    #     print(num, tests)
    #     print(miller_rabin_primality(num, int(log(num)+1)))
    #     print("======")

    print(miller_rabin_primality(123, int(log(123)) + 1))
  