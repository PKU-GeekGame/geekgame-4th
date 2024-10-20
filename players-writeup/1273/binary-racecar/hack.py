import pwn, os

conn = pwn.remote('prob11.geekgame.pku.edu.cn', 10011)
print(conn.recv())
conn.sendline(bytes(os.getenv('TOKEN'), 'ascii'))
print(conn.recv())
conn.sendline(b'1')
print(conn.recv())
conn.send(open('input.bin', 'rb').read()[2:])
print(conn.recv())
print(conn.recv())
print(conn.recv())
print(conn.recv())
