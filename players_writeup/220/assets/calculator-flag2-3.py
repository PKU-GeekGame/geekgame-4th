from pwn import *

code = "(8**(n*n-n)//(8**(2*n-2)-2*8**(n-1)-1))%8**(n-1)" # 48 chars!!!
for lv in [b'2', b'3']:
    print(f"Level {lv}")
    p = remote("prob19.geekgame.pku.edu.cn", 10019)
    p.recvuntil(b"input your token: ")
    p.sendline(b"It's MyToken!!!!!")
    p.recvuntil(b"Level: ")
    p.sendline(lv)
    p.recvuntil(b"Enter your expression: ")
    p.sendline(code.replace(" ", "").encode())
    for l in p.recvall().decode().splitlines():
        print(l)