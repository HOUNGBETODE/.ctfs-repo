from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode
from pwn import *

blocks = lambda text : [text[i:i+AES.block_size] for i in range(0, len(text), AES.block_size)]
cBlocks = lambda ctext : (blocks(b64decode(ctext))[0], blocks(b64decode(ctext))[1:])

ref_plaintext = pad(b"random", AES.block_size)
plaintext = pad(b"I am an authenticated admin, please give me the flag", AES.block_size)
plaintext_blocks = blocks(plaintext)[::-1]

conn = remote("34.162.82.42", 5000)
conn.recvuntil(b"Your choice: ")
conn.sendline(b"1")

chall_ciphertext = conn.recvline()[:-1].decode()
chall_ciphertext_iv, chall_ciphertext_blocks = cBlocks(chall_ciphertext)

# this was quiet an implementation of AES-CBC padding oracle attack on a block.
def findAESCipherBlock(previous, current, IV = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
    bruteforce_block = previous_encrypted_block = previous
    current_encrypted_block = current
    current_decrypted_block = bytearray(IV.encode("ascii"))
    padding = 0
    for j in range(16, 0, -1):
        padding+=1
        for k in range(256):
            bruteforce_block = bytearray(bruteforce_block)
            bruteforce_block[j-1] = (bruteforce_block[j-1] + 1) % 256 # k
            joined_encrypted_block = bytes(bruteforce_block) + current_encrypted_block
            # start exploiting the oracle to be aware whether it's a padding issue or not (via feed_back variable)
            # "Error!" means something goes bad with the padding on decryption
            # "Unknown command!" means the forged ciphertext has been corretly decrypted, and thus padding is correct
            conn.recvuntil(b"Your choice: ")
            conn.sendline(b"2")
            conn.sendline(b64encode(joined_encrypted_block))
            feed_back = conn.recvline()[:-1].decode()
            # print(AES.block_size - j, bruteforce_block[j-1], feed_back)
            if "Error!" in feed_back:
                continue
            elif "Unknown command!" in feed_back:
                current_decrypted_block[-padding] = bruteforce_block[-padding] ^ previous_encrypted_block[-padding] ^ padding
                # Prepare newly found byte values
                for k in range(1, padding+1):
                    bruteforce_block[-k] = padding+1 ^ current_decrypted_block[-k] ^ previous_encrypted_block[-k]
                # print(j, bytes(current_decrypted_block))
                break
    return bytes(current_decrypted_block)


to_give = [xor(chall_ciphertext_iv, ref_plaintext, plaintext_blocks[0]), chall_ciphertext_blocks[0]]
print(f"{to_give = }")

for index in range(1, len(plaintext_blocks)):
    decrypt_value = findAESCipherBlock(chall_ciphertext_iv, to_give[0])
    to_give.insert(0, xor(chall_ciphertext_iv, decrypt_value, plaintext_blocks[index]))
    print(f"{to_give = }")

conn.recvuntil(b"Your choice: ")
conn.sendline(b"2")
conn.sendline(b64encode(b"".join(to_give)))

conn.interactive()