from pwn import *
from Crypto.Util.number import *

context.log_level = "ERROR"

def blockread(r):
    result = b""
    while True:
        _ = r.recvline(timeout=5)
        result += _
        if _ == b"": break
    return result

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

address = "prob07.geekgame.pku.edu.cn"
port = 10007
token = open("token").read().strip()

def parse1(data):
    data = data.decode().split("\n")
    result = {}
    for line in data:
        if ":" in line:
            line = line.split(":")[-1]
        line = line.strip()
        if line.startswith("n = "):
            result['n'] = int(line[4:])
        elif line.startswith("x0 = "):
            result['x0'] = int(line[5:])
        elif line.startswith("x1 = "):
            result['x1'] = int(line[5:])
    print(result)
    return result

def choosev(info):
    n = info['n']
    x0 = info['x0']
    x1 = info['x1']
    return (x0 + x1) // 2

def parse2(data):
    data = data.decode().split("\n")
    result = {}
    for line in data:
        if ":" in line:
            line = line.split(":")[-1]
        if line.startswith("v0 = "):
            result['v0'] = int(line[5:])
        elif line.startswith("v1 = "):
            result['v1'] = int(line[5:])
    print(result)
    return result

def getQ(x0, x1, v0, v1, e, n, v):
    a = (v - x0 + n) % n
    S = (pow(2, e, n) * a % n - pow(v0 - v1, e, n) + n) % n
    if S == 0:
        return None
    q = gcd(S, n)
    return q

def solve(info1, info2, v):
    n = info1['n']
    x0 = info1['x0']
    x1 = info1['x1']
    v0 = info2['v0']
    v1 = info2['v1']
    e = 65537
    q = getQ(x0, x1, v0, v1, e, n, v)
    print(f"n = {n}")
    if q == None:
        print("Failed to get q")
        return None
    print(f"q = {q}")
    p = n // q
    print(f"p = {p}")
    phi = (p - 1) * (q - 1)
    print(f"phi = {phi}")
    d = pow(e, -1, phi)
    f = (v0 - pow(v - x0, d, n) - pow(p + q, d, n) + n + n) % n
    print(f"f = {f}")
    flag = long_to_bytes(f)
    return flag
    

def run():
    r = remote(address, port)
    r.sendline(token.encode())
    blockread(r)
    r.sendline("1".encode())
    part1 = blockread(r)
    info1 = parse1(part1)

    if (info1['x0'] % 2 != info1['x1'] % 2):
        print("x0 and x1 are not in the same parity")
        return None

    v = choosev(info1)
    r.sendline(str(v).encode())
    part2 = r.recvall()
    info2 = parse2(part2)
    flag = solve(info1, info2, v)
    return flag

for _ in range(20):
    flag = run()
    if flag != None:
        print(flag)
        break


