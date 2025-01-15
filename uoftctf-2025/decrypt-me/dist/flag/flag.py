from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
from time import time
import random
random.seed(int(time()))
KEY = SHA256.new(str(random.getrandbits(256)).encode()).digest()
FLAG = "uoftctf{fake_flag}"

def encrypt_flag(flag, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(flag.encode())
    return cipher.nonce + ciphertext

def main():
    encrypted_flag = encrypt_flag(FLAG, KEY)
    with open("flag.enc", "wb") as f:
        f.write(encrypted_flag)

if __name__ == "__main__":
    main()
