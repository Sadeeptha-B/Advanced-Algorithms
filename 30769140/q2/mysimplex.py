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

def tableau_simplex(obj_func, constraint_matrix, rhs):
    no_decisions = len(obj_func) - len(rhs)

    non_basic_idx = [i for i in range(no_decisions)]
    basic_idx = [no_decisions + i for i in range(len(rhs))]

    modified_obj = get_next_basic(basic_idx, obj_func, constraint_matrix)
    



    # print(obj_func)
    # print(constraints_matrix)
    # print(rhs)



    # Return decisions list and optimal value
    return ['5','9'], str(23)

def get_next_basic(basic_idx, obj_func, constraint_matrix):
    maximum, max_ind = float('-inf'), None

    for i in range(len(obj_func)):
        constr_ptr = 0
        row_sum =  0
        for idx in basic_idx:
            row_sum += obj_func[idx] * constraint_matrix[constr_ptr][i]
            constr_ptr += 1

        value = obj_func[i] - row_sum

        if value > maximum:
            maximum = value
            max_ind = i

    return max_ind


def any_positive(lst):
    


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

All returned numbers are floats. The preprocessing is done along with the file reading to avoid 
additional space and time complexity if preprocessing later.
'''
def read_preprocess(filename):
    with open(filename, 'r') as file:
        # No of Decision variables
        file.readline()
        no_decisions = int(file.readline().strip())

        # No of Constraints
        file.readline()
        no_constraints = int(file.readline().strip())

        # Objective function
        file.readline()
        objective = get_padded_lst(file.readline(), no_decisions + no_constraints)

        # Constraints LHS:
        file.readline()

        constraints_matrix = []
        ptr = no_decisions
        
        for _ in range(no_constraints):
            elem = get_padded_lst(file.readline(), no_decisions + no_constraints)
            elem[ptr] = 1.0   # Add slack variable coefficient
            constraints_matrix.append(elem)
            ptr += 1


        # Constraints RHS
        file.readline()
        rhs_values = []

        for _ in range(no_constraints):
            rhs_values.append(float(file.readline().strip()))

    return objective, constraints_matrix, rhs_values


'''
Given a numerical string, will return a list of the specified size with the 
numbers converted to floats. If the specified size is larger than the length 
of the string will pad the specified character
'''
def get_padded_lst(st, size, pad=0.0):
    if st[0] == "#":
        raise ValueError('Expected numerical string')
    
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
    obj_function, constraints_matrix, rhs = read_preprocess(filename)

    # Implement tableau simplex
    decisions,optimal = tableau_simplex(obj_function, constraints_matrix, rhs)

    # # write to file
    # write_output(decisions, optimal)
