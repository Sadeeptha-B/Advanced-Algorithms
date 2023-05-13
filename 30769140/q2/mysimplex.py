'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = "lpsolution.txt"

# Implement Tableau simplex to solve a linear program in it's standard form
# Maximize a given linear objective function involving decision variables that are non
# negative, subject to a set of linear constraints

# Note that the code will need to be generalizable to any number decision variables and 
# constraints

def tableau_simplex(text):
    # Return decisions list and optimal value
    return ['5','9'], str(23)


def read_file(filename):
    pass

def write_output(decisions, optimal):
    headings = ["# optimalDecisions\n", "\n# optimalObjective\n"]
    outputs = [', '.join(decisions), optimal]

    with open(OUTPUT_FILE, 'w') as file:
        for ind, heading in enumerate(headings):
            file.write(heading)
            file.write(outputs[ind])

        

if __name__ == "__main__":
    _, filename = sys.argv

    # Read input format 
    # TODO: change output to be of suitable form for the simplex algorithm
    text = read_file(filename)

    # Implement tableau simplex
    decisions,optimal = tableau_simplex(text)

    # write to file
    write_output(decisions, optimal)




