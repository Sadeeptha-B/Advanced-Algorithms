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


def preprocess_input(objective, constraints):
    

    pass

# I/O operations
# ================================================================================

'''
Reads specified file and preprocesses content to a format suitable for tableau simplex

Returns --------------------------------------------------------------------------
objective: A list with coefficients of the objective function in the provided order,
padded to be the size of decision var + constraints to consider slack variables

constraints_matrix: A list containing constraint lists. The size of a nested list
is (no of decision var + no of constraints) to account for slack variables. The coefficients 
of the slack variables have been added.

rhs_values: A list containing the rhs values in float format

All returned numbers are floats.
'''
def read_preprocess(filename):
    with open(filename, 'r') as file:
        # No of Decision variables
        file.readline()
        decisions = int(file.readline().strip())

        # No of Constraints
        file.readline()
        constraints = int(file.readline().strip())

        # Objective
        file.readline()
        objective = get_padded_lst(file.readline(), decisions + constraints)

        # Constraints LHS
        file.readline()

        constraints_matrix = []
        ptr = decisions
        
        for _ in range(constraints):
            elem = get_padded_lst(file.readline(), decisions + constraints)
            elem[ptr] = 1.0
            constraints_matrix.append(elem)
            ptr += 1

        print(constraints_matrix)

        # Constraints RHS
        file.readline()
        rhs_values = []

        for _ in range(constraints):
            rhs_values.append(float(file.readline().strip()))

        print(rhs_values)

    return constraints, objective, constraints_matrix



'''
Given a numerical string, will return a list of the specified size with the 
numbers converted to floats. If the specified size is larger than the length 
of the string will pad the specified character
'''
def get_padded_lst(st, size, pad=0.0):
    if st[0] == "#":
        raise ValueError()
    
    if type(pad) is not float:
        raise ValueError('Padding must be float')

    res =  st.strip().split(',')

    for i, elem in enumerate(res):
        res[i] = float(elem)

    for _ in range(size - len(res)):
        res.append(pad)

    return res
  
        
def write_output(decisions, optimal):
    headings = ["# optimalDecisions\n", "\n# optimalObjective\n"]
    outputs = [', '.join(decisions), optimal]

    with open(OUTPUT_FILE, 'w') as file:
        for ind, heading in enumerate(headings):
            file.write(heading)
            file.write(outputs[ind])

        

if __name__ == "__main__":
    _, filename = sys.argv

    # Read input 
    text = read_preprocess(filename)

    # Implement tableau simplex
    # decisions,optimal = tableau_simplex(text)

    # # write to file
    # write_output(decisions, optimal)
