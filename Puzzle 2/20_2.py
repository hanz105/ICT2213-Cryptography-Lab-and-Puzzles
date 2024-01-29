import sys, oracle, base64

# Pass the cipher text through decryption algorithm
# Take the first byte of the cipher block and the first byte of the IV and XOR
# Change the value of the IV till it returns the correct padding

def read_from_file(file_path):
    open_file = file_path
    file_stream = open(open_file, encoding='UTF-8')
    read_file = file_stream.read()

    # Removes whitespaces
    read_file = read_file.strip()
    # Decode base64 content
    decoded_file = base64.b64decode(read_file)

    return decoded_file

def multi_block_pad_orac_attack(iv, ciphertext):
    pt = b""
    ct = iv + ciphertext
    block_size = 16
    # Calculate number of blocks in ct with each block size being 16
    num_blocks = len(ct) // block_size

    # Iterate over each block except the last one
    for i in range(num_blocks - 1):
        prev_block = ct[i * block_size: (i + 1) * block_size]
        current_block = ct[(i + 1) * block_size: (i + 2) * block_size]
        decrypted_block = single_block_pad_orac_attack(prev_block, current_block)
        pt += decrypted_block
    
    return pt

def oracle_check(iv_guess, cipherblock):
    test_block = iv_guess + cipherblock
    new_test_b64 = base64.b64encode(test_block)

    return oracle.isPaddingCorrect(new_test_b64) == "Yes"

def single_block_pad_orac_attack(prev_block, curr_block):
    block_size = 16
    intermediate_block = [0] * block_size  # Initialize the intermediate block with zeros
    
    # Iterate over each byte of the block to recover the plaintext
    # First for loop to iterate through the bytes in iv
    for pad_byte in range(1, block_size + 1):
        padding_iv = [pad_byte ^ b for b in intermediate_block]

        # Iterate through each possible value for the current byte
        for i in range(256):
            padding_iv[-pad_byte] = i  # Update padding IV with the current guessed value
            padding_iv_bytes = bytes(padding_iv)  # Convert the IV to bytes

            # Check if the guessed byte value produces correct padding
            if oracle_check(padding_iv_bytes, curr_block):
                # If the padding is correct, update the intermediate block with the recovered byte
                if pad_byte == 1:
                  # Make sure the padding is of length 1 by changing the second last block and querying the oracle again
                    padding_iv[-2] = (padding_iv[-2] + 1) % 255
                    padding_iv_bytes = bytes(padding_iv)
                    if oracle_check(padding_iv_bytes, curr_block):
                        intermediate_block[-pad_byte] = i ^ pad_byte
                        break
                else:
                    intermediate_block[-pad_byte] = i ^ pad_byte
                    break
    
    # Calculate the plaintext by XORing the intermediate block with the previous block
    plaintext = bytes([i ^ b for i, b in zip(intermediate_block, list(prev_block))])
    return plaintext     

iv_contents = read_from_file(sys.argv[1])
ciphertext_contents = read_from_file(sys.argv[2])

# Perform padding oracle attack and retrieve plaintext
final_plaintext = multi_block_pad_orac_attack(iv_contents, ciphertext_contents)
print("Plaintext:", final_plaintext.decode('UTF-8'))