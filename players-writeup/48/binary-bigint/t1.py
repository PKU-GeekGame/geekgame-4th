import numpy as np
import sympy as sp

def byteArray2BigInt(byteArray):
    ans = 0
    base = 0x80
    for c in byteArray:
        ans = ans * base + c
    return ans

def bigInt2String(bigInt):
    base = 0x80
    ans = ""
    while bigInt > 0:
        ans = chr(bigInt % base) + ans
        bigInt //= base
    return ans

A1_ba = [0x65,0x2f,0x2b,0x0f,0x0a,0x6d,0x23,0x7d,0x3d,0x75,0x73,0x7c,0x20,0x57,0x16,0x33,0x42,0x23]
A2_ba = [0x01,0x4c,0x0c,0x37,0x00,0x09,0x07,0x64,0x20,0x4c]
A3_ba = [0x10,0x0a,0x54,0x2a,0x3f,0x72,0x0c,0x4e,0x7e,0x49,0x1d,0x46,0x64,0x44,0x7e,0x31,0x41,0x4a,0x0e,0x41,0x69,0x3c,0x2a,0x00,0x29,0x2d,0x50]

A1 = byteArray2BigInt(A1_ba)
A2 = byteArray2BigInt(A2_ba)
A3 = byteArray2BigInt(A3_ba)

# solve a^3 - A2 * a^2 + A1 * a - A3 = 0
print(A1)
print(A2)
print(A3)

def get_roots():
    a1 = input('a1=')
    a2 = input('a2=')
    a3 = input('a3=')
    return a1, a2, a3

def get_roots_method2():
    a = sp.symbols('a')
    eq = a**3 - A2 * a**2 + A1 * a - A3
    roots = sp.solve(eq, a)
    print(roots)
    for u in roots:
        assert u.is_real
        assert u**3 - A2 * u**2 + A1 * u - A3 == 0
    return roots


a1, a2, a3 = get_roots_method2()


print(bigInt2String(a1))
print(bigInt2String(a2))
print(bigInt2String(a3))