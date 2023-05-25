from mysimplex import TableauSimplex, read_preprocess, get_padded_lst

def get_outputs(filename):
    with open(filename, 'r') as file:
        file.readline()
        decisions = get_padded_lst(file.readline(), 2)
        file.readline()
        optimal = float(file.readline())

    return decisions, optimal
    


if __name__ == "__main__":
    outputs = []
    output_files = [f'../tests/A3_q2_test/lpsolution{i+1}.txt' for i in range(5)]

    for file in output_files:
        outputs.append(get_outputs(file))

    print("Outputs read complete")
    # print(outputs)
    
    input_files = [f'../tests/A3_q2_test/input{i+1}.txt' for i in range(5)]

    for i, file in enumerate(input_files):
        obj, constr, rhs = read_preprocess(file)
        tb = TableauSimplex(obj, constr, rhs)
        decisions, optimal = tb.run()

        if outputs[i] != (decisions, optimal):
            print(f"Fail: file{i+1}")
        # else:
        #     print(decisions, optimal)
        #     print("========")


    print("Success")








