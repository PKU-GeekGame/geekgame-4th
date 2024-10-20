n = int(input())
s = ""
while n > 0:
    s = s + chr(n % 128)
    n //= 128
print(''.join(list(reversed(s))))

# flag{simp1e_cUbIC_39u4710n}