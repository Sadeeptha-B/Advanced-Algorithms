import filecmp
from bwtzip import FileWriter, Encoder
from bwtunzip import BinaryReader, Decoder

# Place test cases in q2_test
files = [f'q2_test/bwtencoded{i}.bin' for i in range(600)]
output_files = [f'q2_test/recovered{i}.txt' for i in range(600)]
myoutput_files = [f'q2_test/myrecovered{i}.txt' for i in range(600)]

for i, file in enumerate(files):
    reader = BinaryReader(file)
    decoder = Decoder(reader)
    txt = decoder.decode()

    output_file = output_files[i]
    myoutput_file = myoutput_files[i] 

    with open(myoutput_file, 'w') as file:
        file.write(txt)

    if not filecmp.cmp(output_file, myoutput_file):
        print(i)
print("Success")