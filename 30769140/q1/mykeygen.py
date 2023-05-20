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



if __name__ == "__main__":
    _, d = sys.argv

    # Validate d to be int


    pass



