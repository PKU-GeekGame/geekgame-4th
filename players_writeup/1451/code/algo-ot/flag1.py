from Crypto.Util.number import long_to_bytes
import math
from hashlib import shake_128
e = 65537
n = int(input('n = '))
x0 = int(input('x0 = '))
x1 = int(input('x1 = '))


if (x0 + x1) % 2 == 0:
    v = (x0 + x1) // 2
    vv = (x1 - x0) // 2
else:
    v = (x0 + x1 + n) // 2
    vv = (x1 - x0 + n) // 2

print(f'{v = }')

v0 = int(input('v0 = '))
v1 = int(input('v1 = '))

c = (pow((v0 - v1), e, n) - pow(2, e, n) * vv) % n
p = math.gcd(c, n)
q = n // p
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
f = (v0 - pow(vv, d, n) - pow(q, d, n) - pow(p, d, n)) % n

fb = long_to_bytes(f)
for i in range(6, 50):
    if fb[:i] + shake_128(fb[:i]).digest(128-i) == fb:
        print(fb[:i])
