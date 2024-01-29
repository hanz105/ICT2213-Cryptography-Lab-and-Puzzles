import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def isPaddingCorrect(ciphertext):
    ct = base64.b64decode(ciphertext)
    iv = b'AAAAAAAAAAAAAAAA'
    key = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    data = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    pt = unpadder.update(data)
    try:
        fin = unpadder.finalize()
    except ValueError:
        return "No"

    return "Yes"