'''
Author: Sadeeptha Bandara
Student ID: 30769140

'''
import sys

OUTPUT_FILE = "output_q1.txt"

'''
Assignment Briefing summary

- Multiple ways of approaching q1
- q2 lesser, in a way that's better. Need a normal bm
implementation first
- 1 mark for answer. 4 for implementation.
- Folder structure. code in one file
- plagiarism penalty
- comments and documentation
- alpha and beta divide
- zalgo and zsuffix
- consider transposition in front, middle and back
- consider transposition from the pattern perspective
- output in text perspective
- optimization: can have zalgo and zsuffix in one output
- output online
- consider one of alpha or beta first, easier from optimization
side. handshake analogy (all about length)
- python file opening
- don't recommend readline because of parsing issues for 
special characters and reading endline char
- argument order be careful

'''


def q1_solution(ref, pat):
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

    q1_solution(text, pattern)    
    