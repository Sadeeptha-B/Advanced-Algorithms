from mykeygen import select_primes    

def read_file(filename):
    with open(filename, 'r') as file:
        file.readline()
        p = int(file.readline().strip())
        file.readline()
        q = int(file.readline().strip())

    return p, q


if __name__ == "__main__":
    file_res = []

    for d in range(100, 2100, 100):
        p, q= read_file(f'../A3_q1_test/tests/secretprimes{d}.txt')
        file_res.append((p,q))

    print('File I/O complete')

    count = 0
    for d in range(100, 2100, 100):
        myp, myq = select_primes(d)
        
        elem = file_res[count]

        if myp != elem[0] or myq != elem[1]:
            print(f"{d}:fail")

        count += 1
        print(d)

    print("Success")
        
