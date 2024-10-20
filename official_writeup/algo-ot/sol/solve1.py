from sage.all import *
from Crypto.Util.number import long_to_bytes
from pwn import *

io = process(['python3', 'task.py'])

io.sendlineafter(b"Please select the level[1/2]: ", b"1")

n, e, x0, x1 = 0, 0, 0, 0
for _ in range(4):
    cmd = io.recvline().decode().strip()
    assert " = " in cmd
    exec(cmd, globals())

# print(n, e, x0, x1)

io.sendlineafter(b"Which message do you want to know?\n", str(x0).encode())

io.recvline()
v0 = int(io.recvline().decode().strip().split(" = ")[1])
v1 = int(io.recvline().decode().strip().split(" = ")[1])

c = pow(v1-v0, e, n) + (x1 - x0) % n

p = gcd(c, n)
assert p != 1
q = n // p
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
f = (v0 - pow(p+q, d, n)) % n
print(long_to_bytes(f))

