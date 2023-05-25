from mykeygen import select_primes  
import timeit  

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
        p, q= read_file(f'../tests/A3_q1_test/secretprimes{d}.txt')
        file_res.append((p,q))

    print('File I/O complete')

    count = 0
    for d in range(100, 2100, 100):
        starttime = timeit.default_timer()
        myp, myq = select_primes(d)
        time = timeit.default_timer() - starttime
        
        elem = file_res[count]

        if myp != elem[0] or myq != elem[1]:
            print(f"{d}:fail")

        count += 1
        print(f"{d}- {time}")

    print("Success")
        
