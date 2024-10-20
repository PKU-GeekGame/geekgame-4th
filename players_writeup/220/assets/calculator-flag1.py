from pwn import *

code = "(0 ** ((19**n - 19) % n)) * (0 ** ((2**n - 2) % n))"
p = remote("prob19.geekgame.pku.edu.cn", 10019)
p.recvuntil(b"input your token: ")
p.sendline(b"It's MyToken!!!!!")
p.recvuntil(b"Level: ")
p.sendline(b"1")
p.recvuntil(b"Enter your expression: ")
p.sendline(code.replace(" ", "").encode())
print(p.recvall())