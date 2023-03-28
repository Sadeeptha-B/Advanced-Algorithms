'''
Author: Sadeeptha Bandara
Student ID: 30769140

'''
import sys

OUTPUT_FILE = "output_q2.txt"

def q2_solution(ref, pat):
    pass

def open_file(filename):
    str = ""

    with open(filename, 'r') as file:
        for line in file:
            str += line.strip()

    return str


def write_output(output):
    with open(OUTPUT_FILE, 'a') as file:
        file.write(f"\n{output}")
        

if __name__ == "__main__":
    _, filename1, filename2 = sys.argv

    text = open_file(filename1)
    pattern = open_file(filename2)

    q2_solution(text, pattern)    
    



