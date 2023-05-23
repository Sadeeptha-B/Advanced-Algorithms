'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys
import random

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
Returns the two smallest prime integers of the form 
2^x - 1 where x >= d
'''
def select_primes(d):
    count = 0
    num = (1 << d) - 1  # 2^x - 1 (x=d)
    res = []

    while count < 2:
        if miller_rabin_primality(num):
            count += 1
            res.append(num)
        num = (num << 1) + 1  # 2^(x+1) - 1 

    return res[0], res[1]


# n > 2
def miller_rabin_primality(n, k):    
    # Special cases
    if n == 2 or n == 3:
        return True
    
    # All even numbers can be returned as non-prime
    if n % 2 == 0:
        return False
    
    s, t = 0, n-1

    while t % 2 == 0:
        s = s + 1
        t = t / 2
    
    for _ in range(k):
        # choose 
        a = random.randint(2, n-2)
        # Loop perfoming congruency check

        # check congruency check at the end if not 1, composite


    return True

'''
n is the product of p and q
'''
def compute_n(p, q):
    return p * q

'''
e is a random integer in the range [3, lambda -1] where 
lambda is 
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
    
    # Select primes of specified form
    p, q = select_primes(d)

    # Compute n and e public keys
    n, e = compute_n(p, q), compute_e(p, q)


    # Write to files
    keyfile_headings = ["# modulus (n)\n", "\n# exponent (e)\n"]
    secretfile_headings = ["# p\n", "\n# q\n"]

    write_to_file(KEY_FILE, keyfile_headings, [n, e])
    write_to_file(SECRET_FILE, secretfile_headings, [p, q])


