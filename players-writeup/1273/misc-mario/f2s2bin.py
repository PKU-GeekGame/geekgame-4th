from sys import stdin

r = bytearray()

for line in stdin:
    t = 0
    if 'R' in line: t += 128
    if 'L' in line: t += 64
    if 'D' in line: t += 32
    if 'U' in line: t += 16
    if 'T' in line: t += 8
    if 'S' in line: t += 4
    if 'B' in line: t += 2
    if 'A' in line: t += 1
    r.append(t)

with open('out.bin', 'wb') as f:
    f.write(r)
