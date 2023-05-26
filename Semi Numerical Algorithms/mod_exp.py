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


if __name__ == "__main__":
    print(mod_exp(7, 560, 561))