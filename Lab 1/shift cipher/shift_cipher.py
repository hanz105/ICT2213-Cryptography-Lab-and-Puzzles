import sys

# Hardcoded frequencies of the letters of the english lang
p = [0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 
     0.02, 0.061, 0.07, 0.001, 0.008, 0.04, 
     0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 
     0.063, 0.09, 0.028, 0.01, 0.024, 0.002,
     0.02, 0.001]

# Reads the files and removes all newline
def read_from_file(file_path):
    with open(file_path, "r") as file:
        text = file.read().replace('\n', '')
    return text

# Calculates the probability of occurrence of every letter in the ciphertext
def probability_ciphertext(text):
    tempList = []
    all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in all_letters:
        tempList.append(text.count(letter))
    for i in range(26):
        tempList[i] /= len(text)
    return tempList

# Calculates the Index of Coincidence for every key shift
# j is the key shift 
# i is the current index of the list, to iterate through every letter probability
def index_of_coincidence(list):
    max = 0
    for j in range(26):
        sum = 0.0
        for i in range(26):
            sum += p[i] * list[(i + j) % 26]
        if sum > max:
            max = sum
            key = j
    return key           

ciphertext = read_from_file(sys.argv[1])
letter_probabilities = probability_ciphertext(ciphertext)
final_key = index_of_coincidence(letter_probabilities)

pt = list(ciphertext)
for i in range(len(pt)):
    pt[i] = chr((ord(pt[i]) - ord('A') - final_key + 26) % 26 + ord('a'))

pt = "".join(pt)
k = chr(final_key + ord('A'))
print(f"\nPlaintext:\n{pt}")
print(f"The key is: {k}")



