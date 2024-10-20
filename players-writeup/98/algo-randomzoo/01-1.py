import os
import time

from pwn import *

os.chdir(os.path.dirname(__file__))

for t in range(0x10):
  conn = remote("prob15.geekgame.pku.edu.cn", 10015)
  conn.recvuntil(b"Please input your token: ")
  conn.send(b"<MY TOKEN>\n")

  writer = open(f"task1-{t:02d}.txt", "w", -1, "utf8", None, "\n")

  for i in range(0x100):
    line = conn.recvline().decode()
    if line:
      writer.write(line)
      writer.flush()
      conn.send(b"\n")

  conn.close()
  writer.close()
  time.sleep(10)
