start = "|1|........|"
input_file = "flag2.fm2"
output_file = "flag2.bin"

# for flag1 should append 1000 ->

f = open(input_file, "r")
f2 = open(output_file, "wb")

while line := f.readline():
    if line.strip().startswith(start):
        break
while line := f.readline():
    dl = line.strip()
    if not dl.startswith("|0|"):
        break
    buttons = dl[3:11]
    byte = 0
    for i in range(8):
        if buttons[i] != ".":
            byte |= 1 << (7 - i)
    f2.write(bytes([byte]))


f2.close()
f.close()
