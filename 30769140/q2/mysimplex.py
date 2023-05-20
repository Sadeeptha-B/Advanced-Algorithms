'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = "lpsolution.txt"


'''
Implements the Tableau Simplex Algorithm to solve a linear problem of the standard
form provided an objective function, constraint matrix and rhs values
'''
def tableau_simplex(obj_func, constraint_matrix, rhs):
    no_decisions = len(obj_func) - len(rhs)

    # Indices of basic variables
    basic_idx = [no_decisions + i for i in range(len(rhs))]

    while True:
        # Index of next basic variable (obj)
        basic_ind = get_next_basic(basic_idx, obj_func, constraint_matrix)
        print(basic_ind)
        if basic_ind is None:
            # Do needful to extract return value
            break

        # Index of variable to fix (constr matrix)
        nonbasic_ind = get_next_non_basic(basic_ind, constraint_matrix, rhs)
        
        if nonbasic_ind is None:
            # No solutions exist
            break

        # put basic_ind at the index of basic_var being removed
        basic_idx[nonbasic_ind] = basic_ind 


        # Divide entire row of new basic_ind and rhs
        basic_row = constraint_matrix[nonbasic_ind]
        coeff = basic_row[basic_ind]

        for i, elem in enumerate(basic_row):
            basic_row[i] = elem / coeff

        rhs[nonbasic_ind] = rhs[nonbasic_ind] / coeff

        # Express all equations wrt basic variables
        for i, constr in enumerate(constraints_matrix):
            if i == nonbasic_ind:
                continue
            basic_coeff = constr[basic_ind]

            # perform element wise math
            for j in range(len(constr)):
                elem = constr[j]
                constr[j] = elem - basic_coeff * basic_row[j]

            rhs[i] = rhs[i] - basic_coeff * rhs[nonbasic_ind]

     
    return ['5','9'], str(23)



### Key point: Constraint rows must match up with corresponding basic variable
'''
Provided the objective function, indices of the basic variables as per the obj function, and the constraint matrix, will perform
row wise dot product between basic variable coefficients in the objective function and the corresponding constraint matrix row.

Will return the index correspdonding to the largest positive value in the modified obj function. If no positive value exists 
returns None
'''
def get_next_basic(basic_idx, obj_func, constraint_matrix):
    maximum, max_ind = float('-inf'), None

    for i in range(len(obj_func)):
        constr_ptr = 0
        row_sum =  0
        for b_id in basic_idx:
            row_sum += obj_func[b_id] * constraint_matrix[constr_ptr][i]
            constr_ptr += 1

        value = obj_func[i] - row_sum

        if value > maximum:
            maximum = value
            max_ind = i

    if maximum <= 0:
        max_ind = None

    return max_ind


'''

'''
def get_next_non_basic(basic_ind, constraint_matrix, rhs):
    minimum, min_ind = float('inf'), None

    for i, r_val in enumerate(rhs):
        basic_coef = constraint_matrix[i][basic_ind]

        # Divide by zero check
        if basic_coef == 0:
            continue 

        value = r_val / basic_coef

        if value < minimum and value > 0:
            minimum = value
            min_ind = i

    return min_ind


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

All returned numbers are floats. The preprocessing is done along with the file reading 
to avoid additional space and time complexity if preprocessing later.
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
of the string will pad with the padding character
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
    # File containing linear program of the standard form
    _, filename = sys.argv

    # Read input 
    obj_function, constraints_matrix, rhs = read_preprocess(filename)

    # Implement tableau simplex
    decisions,optimal = tableau_simplex(obj_function, constraints_matrix, rhs)

    # # write to file
    # write_output(decisions, optimal)
