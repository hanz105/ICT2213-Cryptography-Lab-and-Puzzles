import sys

p = [0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 
     0.02, 0.061, 0.07, 0.001, 0.008, 0.04, 
     0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 
     0.063, 0.09, 0.028, 0.01, 0.024, 0.002,
     0.02, 0.001]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

def decrypt(text, key_slice):
    cipherList = list(text)
    keyList = list(key_slice)
    decryptedList = []
    for i in range(0, len(ciphertext)):
        cipher_char = cipherList[i]
        key_char = keyList[i]
        cipherPosition = alphabet.find(cipher_char)
        keyPosition = alphabet.find(key_char)
        decrypted_char = alphabet[(cipherPosition - keyPosition)]
        decryptedList.append(decrypted_char)
        decrypted_text = "".join(decryptedList)

    return decrypted_text

# Read ciphertext.txt and book.txt
ciphertext = read_from_file(sys.argv[1])
keystream = read_from_file(sys.argv[2])

keyioc_list = []
key_list = []
p_ioc = 0.065

# Retrieve Key Slice
#key_length = len(ciphertext)
for i in range(len(ciphertext) - len(ciphertext) + 1):
    keySlice = keystream[i : (len(ciphertext) + i)]

    # Decrypt ciphertext using current key slice
    decrypted_slice = decrypt(ciphertext, keySlice)

    # Calculate Index of Coincidence of the current plaintext
    letter_probabilities = probability_text(decrypted_slice)
    ioc = 0.0
    for i in range(26):
        ioc += p[i] * letter_probabilities[(i)]

    # Check if the Index of Coincidence is within 0.05 of p_ioc
        #if (ioc > 0.060) and (ioc < 0.070):
    keyioc_list.append(ioc)
    key_list.append(keySlice)

print("keyioc: {}".format(keyioc_list))
print("keylist: {}".format(key_list))
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

#closest_ioc, index = min(enumerate(keyioc_list, key=lambda x: abs(x - p_ioc)))
key = key_list[closest_index]

# Decrypt using the found key
final_plaintext = decrypt(ciphertext, key)

print(final_plaintext)
