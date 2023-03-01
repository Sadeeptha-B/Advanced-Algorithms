import unittest


def z_algorithm():
    pass

class z_algorithm_test(unittest.TestCase):
    
    def setUp(self):
        self.str_input = ["ababac"]

    def test_base_case(self):
        for str in self.str_input:
            z_value = z_algorithm(str)
            # z_value[1]

    
if __name__ == "__main__":
    unittest.main()