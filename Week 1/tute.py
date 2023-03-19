def z_algorithm(str):
    r, l = 0,0
    z_array = [None]*len(str)
    z_array[0] = len(str)
    
    
    for i in range(1, len(str)):
        # Case 1: explicit comparison
        if i > r:
            ptr = i
            count = 0
            while ptr < len(str) and str[i] == str[count]:
                count += 1
                ptr += 1
            
            if count > 0:
                l = i
                r = i + count - 1
            z_array[i] = count

            print(i)


        else:
            k = i - l
            remaining = r - i + 1

            # Case 2a
            if z_array[k] < remaining:
                z_array[i] = z_array[k]
            # Case 2b
            elif z_array[k] > remaining:
                z_array[i] = remaining
            # Case 2c
            else:
                right_ptr = r + 1
                left_ptr = r - i + 1
                count = 0

                while right_ptr < len(str) and str[right_ptr] == str[left_ptr]:
                    count += 1
                    right_ptr += 1
                    left_ptr += 1

                z_array[i] = z_array[k] + count - 1
                l = i
                r = r + count

    return z_array
    
if __name__ == "__main__":
    print(z_algorithm("ababac"))
    print(z_algorithm('aba$bbabaxababay'))






