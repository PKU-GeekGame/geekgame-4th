
fp = open("sunshine.log", "r")

ka = 0
kc = 0
seq = []

while line := fp.readline():
    if line.startswith("keyAction"):
        ka = int(line.split('[')[1].split(']')[0])
    elif line.startswith("keyCode"):
        kc = int(line.split('[')[1].split(']')[0], 16) - 0x8000
        if ka == 3:
            seq.append(kc)

print(seq)

def f(x):
    if x >= 0x20 and x <= 0x7e:
        return chr(x)
    elif x - 0x80 >= 0x20 and x - 0x80 <= 0x7e:
        return chr(x - 0x80)
    else:
        return "?"

s = "".join([f(x) for x in seq])
print(s)