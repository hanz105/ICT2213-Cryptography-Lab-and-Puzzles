import sys

# Hardcoded frequencies for English characters
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

def getSection(index):
    return keystream[index:index+len_ct]

def decryptCT(ct, key):
    # Ascii ct-key to reverse alphabet shift
    newDecrypted = ''
    for i in range(len(ct)):
        newDecrypted += chr(((ord(ct[i]) - ord(key[i])) % 26) + ord('A'))
    return newDecrypted

# Function to compute the key of a ciphertext encrypted by a shift cipher  
def get_ioc(ct):
    # Compute character frequencies for ciphertext ct (array q)
    # Compute counts then divide by size
    q = []
    for letter in alphabet:
        q.append(ct.count(letter))
    for i in range(26):
        q[i] /= len(ct)

    # Compute index of coincidence for different shift values j
    # Key value is maintained into variable key (max IOC)
    ioc = 0
    for i in range(26):
        ioc += p[i]*q[(i)%26]
	
    return ioc

# Read ciphertext.txt and book.txt
ciphertext = read_from_file(sys.argv[1])
keystream = read_from_file(sys.argv[2])

len_ct = len(ciphertext)

max_ioc = 0
possible_key = ''
possible_plaintext = ''
for i in range(len(keystream)-len_ct):
    key = getSection(i)
    possibleMessage = decryptCT(ciphertext,key)
    ioc = get_ioc(possibleMessage)
    if(ioc > max_ioc):
        max_ioc = ioc
        possible_key = key
        possible_plaintext = possibleMessage
    if i > (len(keystream)-len_ct):
        print("Key was not found!")
if max_ioc < 0.060 or max_ioc >= 0.07:
    print("Key was not found!")

#print(max_ioc)
print("Key found: {}".format(possible_key))
print("Plaintext: {}".format(possible_plaintext))
