'''
Author: Sadeeptha Bandara
Student ID: 30769140

Notes:
- The number of tests for Miller Rabin primality is chosen to be floor(ln(n) + 1)
- This choice was made since the probability of a chosen n being prime can be approximated
  to 1/ln(n) for large n
'''


import sys
import random
from math import log
KEY_FILE = "publickeyinfo.txt"
SECRET_FILE = "secretprimes.txt"


'''
Returns the two smallest prime integers of the form 2^x - 1 
where x >= d is a positive integer
'''
def select_primes(d):
    num = (1 << d) - 1  # 2^x - 1 (x=d)
    res = []

    while len(res) < 2:
        confidence = int(log(num) + 1) # Natural logarithm
        
        if miller_rabin_primality(num, confidence):
            res.append(num)

        num = 2 * num + 1  # 2^(x+1) - 1 = 2(2^x-1) + 1

    return res[0], res[1]


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
        current = mod_exp(a, t, num) # Mod exp starting term

        for _ in range(s):

            # Check for first occurence of mod exp becoming 1
            if current == 1:
                if previous != num-1:
                    return False
                else:
                    break

            previous = current
            current = (current ** 2) % num   # Repeated squaring

        # Check fermat's theorem case
        if current != 1 or (current == 1 and previous != num-1):
            return False

    return True


'''
Implements modular exponentiation
'''
def mod_exp(base, exp, div):
     # Indices of significant bits in exp
    exp_places = get_sig_places(exp) 
    
    # Initialized variables for loop
    term = base % div
    sig_ptr = 0
    res= 1

    for i in range(exp.bit_length()):
        if i == exp_places[sig_ptr]:
            res = (res * term) % div
            sig_ptr += 1

        term = (term ** 2) % div

    return res


'''
Euclid's algorithm to compute gcd. Performs mod operation till
b becomes zero.
'''
def compute_gcd(a,b):
    if b == 0:
        return a
    
    return compute_gcd(b, a % b)
    


# Helper methods 
# =============================================================================

'''
Extracts bit by bit from a provided number left to right and then returns
indices of significant bits (bits with value of 1)
'''
def get_sig_places(num):
    bitlen = num.bit_length()
    sig_places = []

    for i in range(bitlen):
        bit = num % 2

        if bit == 1:
            sig_places.append(i)

        num = num >> 1

    return sig_places



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

    d = int(d)
    if d <= 2:
        raise ValueError('d must be larger than 2')

    # Select primes of specified form
    p, q = select_primes(d)
    print(p,q)

    # Compute n and e public keys
    n, e = compute_n(p, q), compute_e(p, q)

    # Write to files
    keyfile_headings = ["# modulus (n)\n", "\n# exponent (e)\n"]
    secretfile_headings = ["# p\n", "\n# q\n"]

    # write_to_file(KEY_FILE, keyfile_headings, [n, e])
    # write_to_file(SECRET_FILE, secretfile_headings, [p, q])


