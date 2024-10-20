from z3 import *

seq = list(map(int, open('seq.txt', 'r').readlines()))
print(f'{len(seq) = }')

def try_length(n):
    s = Solver()
    flag = [BitVec(f'flag_{i}', 8) for i in range(n)]
    s.add(flag[0] == BitVecVal(ord('f'), 8))
    s.add(flag[1] == BitVecVal(ord('l'), 8))
    s.add(flag[2] == BitVecVal(ord('a'), 8))
    s.add(flag[3] == BitVecVal(ord('g'), 8))
    s.add(flag[4] == BitVecVal(ord('{'), 8))
    s.add(flag[n-1] == BitVecVal(ord('}'), 8))
    for i in range(31, len(seq)):
        s.add(Or(
            -flag[i%n] + BitVecVal(seq[i], 8) ==
            -flag[(i-3)%n] + BitVecVal(seq[i-3], 8) +
            -flag[(i-31)%n] + BitVecVal(seq[i-31], 8),

            -flag[i%n] + BitVecVal(seq[i], 8) ==
            -flag[(i-3)%n] + BitVecVal(seq[i-3], 8) +
            -flag[(i-31)%n] + BitVecVal(seq[i-31], 8) + BitVecVal(1, 8)
        ))
    if s.check() == sat:
        return s.model()

