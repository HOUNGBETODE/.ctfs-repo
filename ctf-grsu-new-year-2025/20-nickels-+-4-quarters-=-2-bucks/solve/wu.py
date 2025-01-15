# E : Y^2 = X^3 + a*X + b

from Crypto.Util.number import inverse
from collections import namedtuple
from pwn import *

# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'


def check_point(P: tuple):
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p


def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P: tuple, Q: tuple):
    # based of algo. in ICM
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R


def double_and_add(P: tuple, n: int):
    # based of algo. in ICM
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    assert check_point(R)
    return R



a = b = p = P = Q = R = None
conn = remote("ctf.mf.grsu.by", 9028)

conn.recvuntil(b"Ep(a,b): y^2 = x^3 + ")
res_1 = conn.recvuntil(b"over").decode()
# print(f"{res_1 = }")
a = int(res_1.split("*")[0])
b = int(res_1.split("+ ")[1].split()[0])
p = int(conn.recvline()[:-1].decode().split()[-1])

print(f"{a = }", end=", ")
print(f"{b = }", end=", ")
print(f"{p = }")

conn.recvline()

res_2 = conn.recvline().decode()
# print(res_2)

if "P" in res_2:
    sub = res_2.split("P = (")[1].split(", ")
    P = Point(int(sub[0]), int(sub[1].split(")")[0]))
    print(f"{P = }")

if "Q" in res_2:
    sub = res_2.split("Q = (")[1].split(", ")
    Q = Point(int(sub[0]), int(sub[1].split(")")[0]))
    print(f"{Q = }")

if "R" in res_2:
    sub = res_2.split("R = (")[1].split(", ")
    R = Point(int(sub[0]), int(sub[1].split(")")[0]))
    print(f"{R = }")

loop = int(res_2.split("/ ")[1])
# print(f"{loop = }")

for i in range(loop):
    try:
        if i:
            res_2 = conn.recvline().decode()
            # print(f"{res_2 = }")

            if res_2 == "\n":
                conn.recvuntil(b"Ep(a,b): y^2 = x^3 + ")
                res_1 = conn.recvuntil(b"over").decode()
                # print(f"{res_1 = }")
                a = int(res_1.split("*")[0])
                b = int(res_1.split("+ ")[1].split()[0])
                p = int(conn.recvline()[:-1].decode().split()[-1])

                print(f"{a = }", end=", ")
                print(f"{b = }", end=", ")
                print(f"{p = }")

                conn.recvline()

                res_2 = conn.recvline().decode()
                # print(f"{res_2 = }")

            if "P" in res_2:
                sub = res_2.split("P = (")[1].split(", ")
                P = Point(int(sub[0]), int(sub[1].split(")")[0]))
                print(f"{P = }")

            if "Q" in res_2:
                sub = res_2.split("Q = (")[1].split(", ")
                Q = Point(int(sub[0]), int(sub[1].split(")")[0]))
                print(f"{Q = }")

            if "R" in res_2:
                sub = res_2.split("R = (")[1].split(", ")
                R = Point(int(sub[0]), int(sub[1].split(")")[0]))
                print(f"{R = }")

        step = conn.recvuntil(b" = ")
        # print(f"{step = }")

        op = [eval(f"double_and_add({a.split('*')[1]}, {a.split('*')[0]})") for a in step.decode().split(" = ")[0].split(" + ")]
        res = op[0]
        for point in op[1:]:
            res = point_addition(res, point)
        # print(f"{op = }")
        out = f"{res.x},{res.y}".encode() if res != O else b"None"
        print(f"{step.decode()}{out.decode()}")
        conn.sendline(out)

        conn.recvline()
        conn.recvline()
    except:
        conn.close()

conn.interactive()