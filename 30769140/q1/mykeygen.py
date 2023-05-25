'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys
import random
from math import log


KEY_FILE = "publickeyinfo.txt"
SECRET_FILE = "secretprimes.txt"

# Publicly you share n and e
# n and e is generated with two secret prime numbers


# Task: 
# Select two appropriate primes
#         - p and q are the smallest prime integers of the form 2^x - 1 where x >= d
#         - 2000 >= d > 2 is an input integer 
# Generate n and e from it
#         - n: p * q
#         - e:randomly chosen in the range [3, lambda - 1] such that gcd(e, lambda) = 1
#         - lambda is a complicated eq with p and q
# write primes and public key to two files


'''
Returns the two smallest prime integers of the form 2^x - 1 
where x >= d is a positive integer
'''
def select_primes(d):
    count = 0
    num = (1 << d) - 1  # 2^x - 1 (x=d)
    res = []

    while count < 2:
        confidence = int(log(num) + 1) # Natural logarithm

        if miller_rabin_primality(num, confidence):
            count += 1
            res.append(num)

        num = (num << 1) + 1  # 2^(x+1) - 1 = 2(2^x-1) + 1

    return res[0], res[1]


'''
Performs the fermat test of the form
         a^(n-1) congruent to 1 of congruence class modulo n
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
        
        a = random.randint(2, num - 2)
        previous = num -1
        current = (a ** t) % num   # Mod exp starting term

        for _ in range(s+1):

            # Check for first occurence of mod exp becoming 1
            # If primality test succeeds, breaks loop 
            # If it fails terminates and returns False
            if current == 1:
                if previous != num -1:
                    return False
                else:
                    break

            print(current, )

            previous = current
            current = (current ** 2) % num   # Repeated squaring

    return True

'''
n is the product of p and q
'''
def compute_n(p, q):
    return p * q

'''
e is a random integer in the range [3, lambda -1] where 
lambda is (p-1) * (q-1) / gcd(p-1, q-1)
'''
def compute_e(p, q):
    lda = (p-1)* (q-1)/compute_gcd(p-1, q-1)

    # check the gcd(e, lambda) condition
    e = random.randint(3, lda -1)
    print(compute_gcd(e, lda))

    return e


'''
Euclid's algorithm to compute gcd. Performs mod operation till
b becomes zero.
'''
def compute_gcd(a,b):
    if b == 0:
        return a
    
    return compute_gcd(b, a % b)
    

# I/O operations
# ==============================================================================

def write_to_file(filename, headings, outputs):
    with open(filename, 'w') as file:
        for ind, heading in enumerate(headings):
            file.write(heading)
            file.write(str(outputs[ind]))


if __name__ == "__main__":
    _, d = sys.argv

    # Validate d to be int
    if not d.isdigit():
        raise ValueError('d must be an integer')

    if int(d) <= 2:
        raise ValueError('d must be larger than 2')
    
   
    nums = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461, 252601, 278545, 294409, 314821, 334153]
    for num in nums:
        tests = int(log(num) + 1)
        print(num, tests)
        print(miller_rabin_primality(num, int(log(num)+1)))
        print("======")

    print(miller_rabin_primality(1, int(log(1) + 1)))

    # Select primes of specified form
    # p, q = select_primes(d)

    # # Compute n and e public keys
    # n, e = compute_n(p, q), compute_e(p, q)


    # # Write to files
    # keyfile_headings = ["# modulus (n)\n", "\n# exponent (e)\n"]
    # secretfile_headings = ["# p\n", "\n# q\n"]

    # write_to_file(KEY_FILE, keyfile_headings, [n, e])
    # write_to_file(SECRET_FILE, secretfile_headings, [p, q])


