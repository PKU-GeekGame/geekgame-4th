from Crypto.Util.number import bytes_to_long, getPrime
from secrets import randbelow
from hashlib import shake_128

flag1 = b"fake{flag-1}"
flag2 = b"fake{flag-2}"

def gen():
    e = 65537
    nbits = 1024
    p = getPrime(nbits)
    while p % e == 1:
        p = getPrime(nbits)
    q = getPrime(nbits)
    while q % e == 1:
        q = getPrime(nbits)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return n, e, d, p, q

level = int(input("Please select the level[1/2]: "))
assert level in [1, 2]

n, e, d, p, q = gen()

if level == 1:
    f = bytes_to_long(flag1 + shake_128(flag1).digest(128-len(flag1)))
else:
    f = bytes_to_long(flag2 + shake_128(flag2).digest(128-len(flag2)))

x0 = randbelow(n)
x1 = randbelow(n)

print(f"{n = }")
print(f"{e = }")
print(f"{x0 = }")
print(f"{x1 = }")
print("Which message do you want to know?")

v = int(input("v = "))

if level == 1:
    v0 = (pow(v-x0, d, n) + pow(p+q, d, n) + f) % n
    v1 = (pow(v-x1, d, n) + pow(p-q, d, n) + f) % n
else:
    v0 = (pow(v-x0, d, n) + pow(p+q, d, n) + f) % n
    v1 = (pow(v-x1, d, n) + pow(p-q, d, n) + pow(f, -1, n)) % n

print()
print(f"{v0 = }")
print(f"{v1 = }")

