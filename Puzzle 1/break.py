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

def probability_text(str):
    tempList = []
    all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in all_letters:
        tempList.append(str.count(letter))
    for i in range(26):
        tempList[i] /= len(str)
    return tempList

# Read ciphertext.txt and book.txt
ciphertext = read_from_file(sys.argv[1])
keystream = read_from_file(sys.argv[2])

keyioc_list = []
key_list = []
p_ioc = 0.065
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Retrieve Key Slice
#key_length = len(ciphertext)
for i in range(len(ciphertext)):
    keySlice = keystream[i : (len(ciphertext) + i)]

    # Decrypt ciphertext using current key slice
    encryptedList = list(ciphertext)
    decryptedList = []
    for j in encryptedList:
        cipherchar = j
        cipherPosition = alphabet.find(cipherchar)
        for k in keySlice:
            keychar = k
            keyPosition = alphabet.find(keychar)
        decryptedchar = alphabet[(cipherPosition - keyPosition) % 26]
        decryptedList.append(decryptedchar)
    final_plaintext = "".join(decryptedList)

    # Calculate Index of Coincidence of the current plaintext
    letter_probabilities = probability_text(final_plaintext)
    ioc = 0.0
    for i in range(26):
        ioc += p[i]*letter_probabilities[(i) % 26]

    # Check if the Index of Coincidence is within 0.05 of p_ioc
        #if (ioc > 0.060) and (ioc < 0.070):
    keyioc_list.append(ioc)
    key_list.append(keySlice)

# Find the ioc value that is closest to p_ioc
closest_number = 0.0
min_difference = float('inf')
closest_index = 0
for index, i in enumerate(keyioc_list):
    difference = abs(p_ioc - i)
    if difference < min_difference:
        min_difference = difference
        closest_number = i
        closest_index = index

#print(key_list)
key = key_list[closest_index - 1]

# Decrypt using the found key
encryptedList2 = list(ciphertext)
decryptedList2 = []
for j in encryptedList2:
    cipherchar2 = j
    cipherPosition2 = alphabet.find(cipherchar2)
    for k in key:
        keychar2 = k
        keyPosition2 = alphabet.find(keychar2)
    decryptedchar2 = alphabet[(cipherPosition2 - keyPosition2) % 26]
    decryptedList2.append(decryptedchar2)
final_plaintext2 = "".join(decryptedList2)

print(final_plaintext2)


