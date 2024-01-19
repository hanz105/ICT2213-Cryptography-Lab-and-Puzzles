import sys, math

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

def probability_ciphertext(list):
    tempList = []
    all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in all_letters:
        tempList.append(list.count(letter))
    for i in range(26):
        tempList[i] /= len(list)
    return tempList

def extract_letters_with_interval(text, interval):
    extracted_text = []
    for i in range(0, len(text), interval):
        extracted_text.append(text[i])
    return extracted_text

def get_key_shift(ct):
    # Compute character frequencies for ciphertext ct (array q)
    # Compute counts then divide by size
    q = []
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for letter in alphabet:
        q.append(ct.count(letter))
    for i in range(26):
        q[i] /= len(ct)

    # Compute index of coincidence for different shift values j
    # Key value is maintained into variable key (max IOC)
    max_ioc = 0
    for j in range(26):
        ioc = 0.0
        for i in range(26):
            ioc += p[i]*q[(i+j)%26]

        if ioc > max_ioc:
            max_ioc = ioc
            key = j
	
    return key

ciphertext = read_from_file(sys.argv[1])
q = list(range(26))
s = []
tempList = []
# Assume key length is t
# Then ciphertext can be divided into t parts
# First for loop is the key length
# Nested for loop is the alphabet frequency percentage for that key length
for k in range(1, 26, 1):
    # Set all letter frequencies for current key length to 0
    for i in range(26):
        q[i] = 0.0

    # Extract ciphertext at regular intervals
    # Store it in tempList
    tempList.clear()
    tempList = extract_letters_with_interval(ciphertext, k)

    # Calculate the frequencies for all letters in the extracted ciphertext
    #for i in range(len(tempList)):
    q = probability_ciphertext(tempList)

    # Calculate the Index of Coincidence and store it into list s
    ioc = 0.0
    for i in range(26):
        ioc += q[i] * q[i]
    s.append(ioc)

for i in range(25):
    print(f"{i}: {s[i]}")

# Compute the 3 largest jumps in list s and then get their gcd
# This will be the key length (might not always work)
diff = [0]
max1 = max2 = max3 = 0
for i in range (24):
    diff.append(s[i + 1] / s[i])
for i in range(25):
    if diff[i] > max1:
        max1 = diff[i]
        i1 = i + 1
for i in range(25):
    if diff[i] > max2 and diff[i] != max1:
        max2 = diff[i]
        i2 = i + 1
for i in range(25):
    if diff[i] > max3 and diff[i] != max1 and diff[i] != max2:
        max3 = diff[i]
        i3 = i + 1
length = math.gcd(i1, i2)
length = math.gcd(length, i3)
            
# Extract length sequences and, for each one, brute-force the shift key
key = []
for k in range(length):
    tmp = []
    for i in range(k,len(ciphertext),length):
        tmp.append(ciphertext[i])
    key.append(get_key_shift(tmp))

# Decrypt the ciphertext, where the i-th character is shifted by key[i%length] positions
pt = list(ciphertext)
for i in range(len(pt)):
    pt[i] = chr((ord(pt[i]) - ord('A') - key[i%length] + 26) % 26 + ord('a'))

# Print plaitext and key
pt = "".join(pt)
print (f"Plaintext:\n{pt}")
for i in range(length):
    key[i] = chr(key[i] + ord('A'))
key = "".join(key)
print (f"Key: {key}")

