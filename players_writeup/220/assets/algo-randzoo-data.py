from pwn import *

p = remote('prob17.geekgame.pku.edu.cn', 10017)
p.recvuntil(b"input your token: ")
p.sendline(b"It's MyToken!!!!!")
with open("./randzoo-nums.txt", "wb") as f:
    for _ in range(800):
        p.send(b'\n')
        f.write(p.recvline())
with open("./randzoo-input.txt", "w") as f:
    with open("./randzoo-nums.txt", "r") as g:
        for c in 'flag{':
            f.write(str(int(g.readline()) - ord(c)))
            f.write("\n")