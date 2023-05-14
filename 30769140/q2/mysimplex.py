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
    with open(filename, 'r') as file:
        # Decision variables
        file.readline()
        decisions = int(file.readline().strip())

        # Constraints
        file.readline()
        constraints = int(file.readline().strip())

        # Objective
        file.readline()
        objective = str_to_lst(file.readline(), decisions)

        # Constraints LHS
        file.readline()
        
        constraints_matrix = [[None, None] for _ in range(constraints)]
        LHS_IND = 0
        RHS_IND = 1

        for i in range(constraints):
            constraints_matrix[i][LHS_IND] = str_to_lst(file.readline(), decisions)

        # Constraints RHS
        file.readline()

        for i in range(constraints):
            constraints_matrix[i][RHS_IND] = int(file.readline().strip())


    return decisions, constraints, objective, constraints_matrix


def str_to_lst(st, decisions):
    if st[0] == "#":
        raise ValueError()

    res =  st.strip().split(',')

    if len(res) != decisions:
        raise ValueError('No of coefficients should be same as number of decision variables')

    return [int(v) for v in res]

      
        
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
    # decisions,optimal = tableau_simplex(text)

    # # write to file
    # write_output(decisions, optimal)
