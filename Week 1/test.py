import unittest
import random
import timeit
from main import z_algorithm_pattern_match
from z_algo import z_algo

def generate_string(n, p):
    alphabet = ('H', 'T')
    str_array = [0] * n

    for i in range(len(str_array)):
        str_array[i] = random.choices(alphabet, weights=(p, 1-p))[0]

    str = ''.join(str_array)
    
    with open('rand_string.txt', "a") as file:
        file.write(str + '\n')

def generate_inputs():
    str_sizes = [1000000]
    probs = [0.2, 0.5, 0.8]

    for size in str_sizes:
        for prob in probs:
            generate_string(size, prob)

def time_execution():
    with open('rand_string.txt', 'r') as f:
        for line in f:
            str = line.strip()
            start_time = timeit.default_timer()
            z_algorithm_pattern_match(str)
            print(f"Time elapsed: {timeit.default_timer() - start_time}")


class z_algorithm_test(unittest.TestCase):
    
    def setUp(self):
        self.str_input = ["ababac"]

    def test_base_case(self):
        # for str in self.str_input:
        #     z_value = z_algorithm(str)
            # z_value[1]
        pass

'''
Credits to Satya Jhaveri for the test cases

'''
def test_z_alg() -> None:    
    word="acbaa"
    expected = [None, 0, 0, 1, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acbaa!\n\tExpected:[None, 0, 0, 1, 1]\n\tActual:{z_algo(word)}")

    word="bbacbbabab"
    expected = [None, 1, 0, 0, 3, 1, 0, 1, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbacbbabab!\n\tExpected:[None, 1, 0, 0, 3, 1, 0, 1, 0, 1]\n\tActual:{z_algo(word)}")

    word="acbacbccbababacbccba"
    expected = [None, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acbacbccbababacbccba!\n\tExpected:[None, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="babbbabccbacccbbaacb"
    expected = [None, 0, 1, 1, 3, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for babbbabccbacccbbaacb!\n\tExpected:[None, 0, 1, 1, 3, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="bccaacaccb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bccaacaccb!\n\tExpected:[None, 0, 0, 0, 0, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="bccbcccbaacaabacccac"
    expected = [None, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bccbcccbaacaabacccac!\n\tExpected:[None, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]\n\tActual:{z_algo(word)}")

    word="ccbbababca"
    expected = [None, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for ccbbababca!\n\tExpected:[None, 1, 0, 0, 0, 0, 0, 0, 1, 0]\n\tActual:{z_algo(word)}")

    word="acccbcbcca"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acccbcbcca!\n\tExpected:[None, 0, 0, 0, 0, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="abcaabcaac"
    expected = [None, 0, 0, 1, 5, 0, 0, 1, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for abcaabcaac!\n\tExpected:[None, 0, 0, 1, 5, 0, 0, 1, 1, 0]\n\tActual:{z_algo(word)}")

    word="bbcccbabbaccbcbcacab"
    expected = [None, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbcccbabbaccbcbcacab!\n\tExpected:[None, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="acacbcbbabcbaca"
    expected = [None, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acacbcbbabcbaca!\n\tExpected:[None, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 1]\n\tActual:{z_algo(word)}")

    word="cbbcaaccccbbccb"
    expected = [None, 0, 0, 1, 0, 0, 1, 1, 1, 4, 0, 0, 1, 2, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for cbbcaaccccbbccb!\n\tExpected:[None, 0, 0, 1, 0, 0, 1, 1, 1, 4, 0, 0, 1, 2, 0]\n\tActual:{z_algo(word)}")

    word="bbabc"
    expected = [None, 1, 0, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbabc!\n\tExpected:[None, 1, 0, 1, 0]\n\tActual:{z_algo(word)}")

    word="bbabacacbacbaacacbbb"
    expected = [None, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbabacacbacbaacacbbb!\n\tExpected:[None, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 1]\n\tActual:{z_algo(word)}")

    word="bbbbbccaccbbabb"
    expected = [None, 4, 3, 2, 1, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbbbbccaccbbabb!\n\tExpected:[None, 4, 3, 2, 1, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1]\n\tActual:{z_algo(word)}")

    word="accbbabacaabcbaaaccb"
    expected = [None, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 1, 1, 4, 0, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for accbbabacaabcbaaaccb!\n\tExpected:[None, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 1, 1, 4, 0, 0, 0]\n\tActual:{z_algo(word)}")

    word="accaaabcacbacba"
    expected = [None, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for accaaabcacbacba!\n\tExpected:[None, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="bbacababcaaacbcbcbaa"
    expected = [None, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbacababcaaacbcbcbaa!\n\tExpected:[None, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]\n\tActual:{z_algo(word)}")

    word="bcacabbacaaaaba"
    expected = [None, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bcacabbacaaaaba!\n\tExpected:[None, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]\n\tActual:{z_algo(word)}")

    word="baaabaabbbbacccaabaa"
    expected = [None, 0, 0, 0, 3, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for baaabaabbbbacccaabaa!\n\tExpected:[None, 0, 0, 0, 3, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0]\n\tActual:{z_algo(word)}")
    
if __name__ == "__main__":
    # unittest.main()
    # generate_string(5, 0.3)
    # generate_inputs()
    # z_algorithm_pattern_match('bbabaxababay', 'aba')
    # time_execution();
    test_z_alg();
