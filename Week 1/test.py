import unittest
import random
import timeit
from algorithms import z_algorithm_pattern_match

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
    start_time = timeit.default_timer()
    print("Start time")
    z_algorithm_pattern_match()
    print(f"Time elapsed: {timeit.default_timer() - start_time}")


class z_algorithm_test(unittest.TestCase):
    
    def setUp(self):
        self.str_input = ["ababac"]

    def test_base_case(self):
        # for str in self.str_input:
        #     z_value = z_algorithm(str)
            # z_value[1]
        pass

    
if __name__ == "__main__":
    # unittest.main()
    # generate_string(5, 0.3)
    # generate_inputs()
    # z_algorithm_pattern_match('bbabaxababay', 'aba')
    pass
