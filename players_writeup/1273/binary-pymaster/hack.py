import base64
from subprocess import run,PIPE

def fun(flg):
    r = run(f'python3.8 pyhacker.py <<<"{flg}"', shell=True, stdout=PIPE, encoding='utf8').stdout.strip()
    print(f'{flg} -> {r}')
    return list(map(lambda s: int(s, 16), r.split()))

f = 'flag{123456789012345678901234567890}'
a = fun(f)

idx = []
for i in range(36):
    ff = f[:i] + 'X' + f[i+1:]
    aa = fun(ff)
    for j in range(36):
        if aa[j] != a[j]:
            idx.append(j)
print(idx)

target = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
print(' '.join(f'{c:02x}' for c in target))

lis=[i for i in range(36) if target[i] != a[i]]
lis.sort()
print(lis)

for i in range(36):
    if a[i] != target[i]:
        pp = idx.index(i)
        f = f[:pp] + chr(ord(f[pp]) ^a[i] ^ target[i]) + f[pp+1:]
print(f)
