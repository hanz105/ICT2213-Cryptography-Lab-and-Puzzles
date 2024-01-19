import sys

p = [0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 
     0.02, 0.061, 0.07, 0.001, 0.008, 0.04, 
     0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 
     0.063, 0.09, 0.028, 0.01, 0.024, 0.002,
     0.02, 0.001]

def read_from_file(file_path):
    open_file = file_path
    file_stream = open(open_file, encoding='UTF-8')
    read_file = file_stream.read()

    for char in read_file:
        if not char.isalpha():
            read_file = read_file.replace(char, '')
    upper_case = read_file.upper()

    return upper_case


ciphertext = read_from_file(sys.argv[1])
keystream = read_from_file(sys.argv[2])

# Find the length of the ciphertext (513)
ciphertext_length = len(ciphertext)
