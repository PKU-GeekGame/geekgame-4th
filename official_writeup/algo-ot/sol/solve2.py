from sage.all import *
from Crypto.Util.number import long_to_bytes
from pwn import *

n, e, x0, x1 = 0, 0, 0, 0

R0 = PolynomialRing(ZZ, 'x')
x = R0.gen()

def run_once():
    io = process(['python3', 'task.py'])

    io.sendlineafter(b"Please select the level[1/2]: ", b"2")
    
    for _ in range(4):
        cmd = io.recvline().decode().strip()
        assert " = " in cmd
        exec(cmd, globals())

    # print(n, e, x0, x1)

    io.sendlineafter(b"Which message do you want to know?\n", str(mod(x0+x1, n) / 2).encode())

    io.recvline()
    v0 = int(io.recvline().decode().strip().split(" = ")[1])
    v1 = int(io.recvline().decode().strip().split(" = ")[1])
    io.close()

    poly = x**2 + 1 - (v0 + v1) * x
    return poly, n

polys, ns = zip(*[run_once() for _ in range(6)])
MOD = prod(ns)
b = crt([poly.list()[1] for poly in polys], list(ns))

R = PolynomialRing(Zmod(MOD), 'x')
x = R.gen()
poly = x**2 + 1 + b * x

f = poly.small_roots(X=2**1024, beta=0.49, epsilon=0.04)[0]

print(long_to_bytes(int(f)))

