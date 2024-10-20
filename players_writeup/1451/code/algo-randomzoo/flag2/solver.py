from z3 import *
import sys

data = []

file_name = "./true_data.txt"
# file_name = "./test_data.txt"

with open(file_name, "r") as f:
    for line in f.readlines():
        item = int(line.strip())
        # print(item)
        data.append(item)


solver = Solver()

print(sys.argv)
GUESS_NUM = int(sys.argv[1])
EQ_NUM = GUESS_NUM * 2


def z3_state_to_number(y):
    y = y ^ LShR(y, 11)
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ LShR(y, 18)
    return y & 0xffffffff


flag = [BitVec(f'c{i}', 32) for i in range(GUESS_NUM)]

for c in flag:
    solver.add(c >= 0x0, c <= 0x7e)

solver.add(
    flag[0] == ord('f'),
    flag[1] == ord('l'),
    flag[2] == ord('a'),
    flag[3] == ord('g'),
    flag[4] == ord('{'),
    # flag[GUESS_NUM - 1] == ord('}'),
)

state_dict = {}

for i in range(EQ_NUM):
    for idx in (i, i + 1, i + 397, i + 624):
        if idx not in state_dict:
            state_dict[idx] = BitVec(f's{idx}', 32)


for i in range(EQ_NUM):
    s0 = state_dict[i]
    s1 = state_dict[i + 1]
    s397 = state_dict[i + 397]
    s624 = state_dict[i + 624]
    solver.add(
        z3_state_to_number(s0) + flag[i % GUESS_NUM] == data[i],
        z3_state_to_number(s1) + flag[(i + 1) % GUESS_NUM] == data[i + 1],
        z3_state_to_number(s397) + flag[(i + 397) % GUESS_NUM] == data[i + 397],
        z3_state_to_number(s624) + flag[(i + 624) % GUESS_NUM] == data[i + 624],
    )
    y = ((s0 & 0x80000000) + (s1 & 0x7fffffff)) & 0xFFFFFFFF
    solver.add(Implies(y & 1 != 0, s624 == LShR(y, 1) ^ s397 ^ 0x9908b0df))
    solver.add(Implies(y & 1 == 0, s624 == LShR(y, 1) ^ s397))


if solver.check() == sat:
    model = solver.model()
    rst = ""
    for i in range(GUESS_NUM):
        rst += chr(model[flag[i]].as_long())

    print([rst])
    for k, v in sorted(state_dict.items(), key=lambda x: x[0]):
        print(f"state {k}: {model[v].as_long()}")

else:
    print("G!")
