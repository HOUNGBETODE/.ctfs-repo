from pwn import *
import string

blocks = lambda hexB : [bytes.fromhex(hexB[i:i + 32]) for i in range(0, len(hexB), 32)]

def sendData(conn, data):
    conn.recvuntil(b"> (hex) ")
    conn.sendline(data.hex().encode())
    conn.recvuntil(b" Here is your encryption:\n|\n|   ")
    return blocks(conn.recvline()[:-1].decode())


flag = ''
poss_chars = string.ascii_letters + string.punctuation + string.digits
conn = remote('confusion.challs.srdnlen.it', 1338)


for i in range(95, -1, -1):
    ref = sendData(conn, data = b"a"*i)[6]

    for c in poss_chars:
        pt_c = ("a"*(i%16) + flag + c).encode()
        ct_c = sendData(conn, data = pt_c)[1]
        #
        ref_0 = sendData(conn, data = f"{'a'*i}{flag}{c}".encode())[6]
        
        if xor(ref, pt_c, ct_c) == xor(ref_0, pt_c, ct_c):
            flag+=c
            print(f"{flag = }")

            if c == "}":
                exit()
            else:
                break


conn.close()