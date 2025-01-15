import random
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def decrypt_flag(encrypted_flag, key):
    nonce = encrypted_flag[:16]
    ciphertext = encrypted_flag[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode("latin1")


seed_ = datetime(2025, 1, 6, 3, 13, 39).timestamp() # timestamp extraction from modification datetimes
print(f"{seed_ = }")
encrypted_flag = open("../dist/flag/flag.py:flag.enc:$DATA", "rb").read()

iterator = 0
while True:
    random.seed(seed_ + iterator)
    KEY = SHA256.new(str(random.getrandbits(256)).encode()).digest()
    try:
        flag_to_be_ = decrypt_flag(encrypted_flag, KEY)
        if "uoftctf".lower() in flag_to_be_.lower():
            print(f"{flag_to_be_ = }")
            break
    except:
        pass
    iterator+=1