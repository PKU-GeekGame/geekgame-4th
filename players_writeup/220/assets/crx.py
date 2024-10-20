from pwn import *
import builtins
sh = remote('prob02.geekgame.pku.edu.cn', 10002)
# sh = process('./binary-rtree/lv1/rtree')
sh.recvuntil(b"input your token: ")
sh.sendline(b"It's MyToken!!!!!")

ATKHTML = open("./crx.html", "r").read()  

sh.send(ATKHTML.encode())
sh.send(b'EOF\n')
while l := sh.recvline():
    print(l.decode())