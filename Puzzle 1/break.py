import sys

p = [0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 
     0.02, 0.061, 0.07, 0.001, 0.008, 0.04, 
     0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 
     0.063, 0.09, 0.028, 0.01, 0.024, 0.002,
     0.02, 0.001]

# Opens the file as a string, removes all punctuation and spaces, and make everything upper case
def read_from_file(file_path):
    open_file = file_path
    file_stream = open(open_file, encoding='UTF-8')
    read_file = file_stream.read()

    for char in read_file:
        if not char.isalpha():
            read_file = read_file.replace(char, '')
    upper_case = read_file.upper()

    return upper_case

def probability_ciphertext(str):
    tempList = []
    all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in all_letters:
        tempList.append(str.count(letter))
    for i in range(26):
        tempList[i] /= len(str)
    return tempList

def calculate_ioc(ciphertext_percent):
    #max_ioc = 0
    #for j in range(26):
    ioc = 0.0
    for i in range(26):
        ioc += p[i] * ciphertext_percent[(i) % 26]

        # if ioc > max_ioc:
        #     max_ioc = ioc
        #     key = j
	
    return ioc

ciphertext = read_from_file(sys.argv[1])
keystream = read_from_file(sys.argv[2])
key_length = len(ciphertext)
ct_probabilities_list = probability_ciphertext(ciphertext)
#print(ct_probabilities_list)

# Retrieve Key Slice
max_ioc = 0
for i in range(key_length):
    keySlice = keystream[i : (key_length + i)]
    # Calculate Index for Coincidence for current key slice
    ioc = 0.0
    for i in range(26):
        ioc += p[i] * ct_probabilities_list[(i) % 26]
        
        if ioc > max_ioc:
            max_ioc = ioc
            key = keySlice

print(key)


    #print("Key {0}: {1}".format(i, keySlice))
    # formatted_key_slice = "key slice {0}: {1}".format(i, keySlice)
    # text_file = open("test.txt", "w", encoding='UTF-8')
    # n = text_file.write(formatted_key_slice + '\n')
    # if n == len(formatted_key_slice):
    #     print("Success")
    # else:
    #     print("Nah")

# Find the length of the ciphertext (513)
#ciphertext_length = len(ciphertext)
#print(ciphertext_length)

# Checking keyList
# for i in range(10):
#     print("Key {}: {}".format(i, keyList[i]))

