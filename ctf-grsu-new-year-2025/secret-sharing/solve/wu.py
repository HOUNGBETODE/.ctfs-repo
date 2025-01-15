from pwn import *
from math import gcd
import numpy as np
from sympy import Matrix

conn = remote("ctf.mf.grsu.by", 9040)

while True:
    try:
        conn.recvuntil(b"n: ")
        n = int(conn.recvline()[:-1].decode())

        conn.recvuntil(b"k: ")
        k = int(conn.recvline()[:-1].decode())

        conn.recvuntil(b"prime: ")
        prime = int(conn.recvline()[:-1].decode())

        print(f"{n = }")
        print(f"{k = }")
        print(f"{prime = }")

        conn.recvline()
        conn.recvline()

        shares = []
        for i in range(n):
            rec = conn.recvline()
            # print(rec)
            shares.append(int(rec[:-1].decode().split(", ")[1].split(")")[0]))
        # print(f"{shares = }")

        mat_shares = Matrix(np.array([[x**i for i in range(n)] for x in range(1,n+1)])).inv_mod(prime)

        if n==k:
            white_numbers = np.dot(np.array(mat_shares), np.array(shares)) % prime
        else:
            for i in range(1, len(shares)+1):
                shares[i-1] = (shares[i-1] + sum((i ** j) for j in range(k, n))) % prime
            white_numbers = np.dot(np.array(mat_shares), np.array(shares)) % prime

        print(f"{white_numbers[0] = }")

        conn.recvuntil(b"secret: ")
        conn.sendline(f"{white_numbers[0]}".encode())
        
    except:
        conn.interactive()