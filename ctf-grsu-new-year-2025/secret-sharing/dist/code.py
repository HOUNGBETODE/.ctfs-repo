#! /usr/bin/python3 -u

import random
from random import randint
from sympy import symbols, mod_inverse
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes
import json
from secret import secret, flag


def generate_shares(secret, n, k, prime):
    """
    Generates N shares using Shamir's (N, k)-scheme.
    """
    if k > n:
        raise ValueError("k must be less than or equal to n")
    
    # Generating random coefficients for a polynomial
    coefficients = [secret] + [random.randint(1, prime - 1) for _ in range(k - 1)]
    
    # Polynomial function f(x)
    def polynomial(x):
        return sum(coefficients[i] * (x ** i) for i in range(k)) % prime

    # Generate shares
    shares = [(i, polynomial(i)) for i in range(1, n + 1)]
    return shares


def print_shares(shares):
    for share in shares:
        print(f"Share: {share}")


secret = getPrime(512)  # Secret number
n = randint(5,10)          # Number of shares
k = randint(2,n)           # Minimum number of shares to restore the secret
prime = getPrime(1024)     # Prime number, larger than the secret
print (f"n: {n}\nk: {k}\nprime: {prime}\n\n")

shares = generate_shares(secret, n, k, prime)
print_shares(shares)
print()
print ("secret: ", end="")

answer = input()           # Your answer
if answer == secret:
    print (f"Flag: {flag}")
