'''
Author: Sadeeptha Bandara
Student ID: 30769140
'''

import sys

OUTPUT_FILE = "lpsolution.txt"


'''
Implements the Tableau Simplex Algorithm to solve a linear problem of the standard
form provided an objective function, constraint matrix and rhs values

obj_func: List of size decision var + constraints. With slack variables as zeros
constr_matrix: List of constraints length containing lists of the obj func length,
               each corresponding to a constraint
rhs: List containing RHS values to the constraints

All values should be provided as floats.
'''

class TableauSimplex():
    def __init__(self, obj_func, constr_matrix, rhs) -> None:
        self.obj_func = obj_func
        self.constr_matrix = constr_matrix
        self.rhs = rhs


    def run(self):
        obj_func = self.obj_func
        rhs = self.rhs
        no_decisions = len(obj_func) - len(rhs)

        # Indices of basic variables
        basic_idx = [no_decisions + i for i in range(len(rhs))]

        while True:
            # Index of variable to make a basic variable
            basic_ind = self.get_next_basic(basic_idx)

            if basic_ind is None: 
                res = [0] * no_decisions

                for i, elem in enumerate(basic_idx):
                    if elem < no_decisions:
                        res[elem] = rhs[i]

                sum = 0
                for i in range(len(obj_func)):
                    sum += obj_func[i] * res[i]


            # Index of variable to make nonbasic
            nonbasic_ind = self.get_next_nonbasic(basic_ind)
            
            if nonbasic_ind is None:
                # No solutions exist
                break

            basic_idx[nonbasic_ind] = basic_ind 

            # Express all equations considering new basic variable
            self.compute_next_eqns(nonbasic_ind, basic_ind)


        return res, sum

    '''
    Return the index of the variable that should be the new incoming basic variable
    (Index as per obj function)
    '''
    def get_next_basic(self, basic_idx):
        obj_func = self.obj_func
        constr_matrix = self.constr_matrix

        maximum, max_ind = float('-inf'), None

        for i in range(len(obj_func)):
            constr_ptr = 0
            row_sum =  0

            # Perform column-wise dot product
            for b_id in basic_idx:
                row_sum += obj_func[b_id] * constr_matrix[constr_ptr][i]
                constr_ptr += 1

            value = obj_func[i] - row_sum

            if value > maximum:
                maximum = value
                max_ind = i

        if maximum <= 0:
            max_ind = None

        return max_ind

    '''
    Returns the index of the variable to be removed from the basis 
    (Index as per constr matrix)
    '''
    def get_next_nonbasic(self, basic_ind):
        constr_matrix = self.constr_matrix
        rhs = self.rhs
        minimum, min_ind = float('inf'), None

        for i, r_val in enumerate(rhs):
            basic_coef = constr_matrix[i][basic_ind]

            # Divide by zero check
            if basic_coef == 0:
                continue 

            value = r_val / basic_coef

            if value < minimum and value > 0:
                minimum = value
                min_ind = i

        return min_ind


    '''
    Given
    nonbasic_ind: Index of the constraint containing the variable to be removed 
                from basis
    basic_ind: Index of the variable to be added to basis 
    
    will mutate constr matrix and RHS as per the new basic variable
    '''
    def compute_next_eqns(self, nonbasic_ind, basic_ind):
        constr_matrix = self.constr_matrix
        rhs = self.rhs

        # Row containing new basic variable
        basic_row = constr_matrix[nonbasic_ind]
        coeff = basic_row[basic_ind]

        for i, elem in enumerate(basic_row):
            basic_row[i] = elem / coeff

        rhs[nonbasic_ind] = rhs[nonbasic_ind] / coeff

        # Mutate other constraints
        for i, constr in enumerate(constr_matrix):
            if i == nonbasic_ind:
                continue
            basic_coeff = constr[basic_ind]

            for j in range(len(constr)):
                elem = constr[j]
                constr[j] = elem - basic_coeff * basic_row[j]

            rhs[i] -= basic_coeff * rhs[nonbasic_ind]



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
    obj_function, constraints_matrix, rhs_values = read_preprocess(filename)

    # Implement tableau simplex
    tb = TableauSimplex(obj_function, constraints_matrix, rhs_values)
    decisions, optimial = tb.run()

    # # write to file
    # write_output(decisions, optimal)
