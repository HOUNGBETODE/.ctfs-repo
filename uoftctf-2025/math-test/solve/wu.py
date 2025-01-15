from pwn import *

conn = remote("34.66.235.106", 5000)

for i in range(1000):
    conn.recvuntil(b"Question: ")
    ope = conn.recvline()[:-1].decode()
    ans = eval(ope)
    # print(i, ope, ans)
    conn.recvuntil(b"Answer: ")
    conn.sendline(str(ans).encode())

conn.interactive()