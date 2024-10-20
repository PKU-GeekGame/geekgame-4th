import z3, time

vec = []
rngLen = 607
slice_len = 2466
# slice_len = 1214
mask = sum([(1 << i) for i in range(16, 31)])

def seed():
    global vec
    vec = [z3.BitVec(f'vec_{i}', 65) for i in range(rngLen)]
    # vec = [z3.Int(f"vec_{i}") for i in range(rngLen)]

def solve(slice):
    global vec
    s = z3.Solver()
    for i in range(len(slice)):
        # rng_ret = uint32()
        ref = slice[i]
        # 16 bits at a time, 2466 * 16 > 607 * 65
        # s.add(z3.LShR(rng_ret, 16) == (ref >> 16))
        match_16_bytes(ref, s)
    print("Modeled.")
    print(s)
    start = time.time()
    if s.check() != z3.sat:
        print("Unsat!")
        return None
    m = s.model()
    end = time.time()
    print("Pred! Time:", end - start)
    return m

def uint64():
    global vec
    vec = [vec[-1]] + vec[:-1]
    vec[334] = (vec[0] + vec[334]) & ((1 << 64) - 1)
    return vec[334]

def match_16_bytes(actual, solver):
    ret = uint64()
    for i in range(0, 32):
        actual_bit = (actual >> i) & 1
        exp_bit_pos = i + 31
        solver.add(z3.Extract(exp_bit_pos, exp_bit_pos, ret) == actual_bit)

# def uint32():
#     # return (uint64() & ((1 << 63) - 1)) >> 31
#     return z3.LShR((uint64() & ((1 << 63) - 1)), 31)

def model_uint64(model):
    global vec
    vec = [vec[-1]] + vec[:-1]
    vec[334] = (vec[0] + vec[334]) & ((1 << 63) - 1)
    return model.eval(vec[334])

def model_uint32(model):
    return (model_uint64(model) & ((1 << 63) - 1)) >> 31

def main():
    with open("2e5.out", "r") as f:
        ints = [int(x.strip()) for x in f.readlines()]
    ints_ptr = 0
    out_model = None
    ok = False
    while not ok:
        while out_model is None:
            seed()
            slice = ints[ints_ptr:ints_ptr + slice_len]
            ints_ptr += slice_len
            out_model = solve(slice)
        out_bytes = bytearray()
        for _ in range(100):
            ref = model_uint32(out_model)
            actual = ints[ints_ptr]
            ints_ptr += 1
            chr = actual - ref
            if chr < 0 or chr > 126:
                break
            out_bytes.append(chr)
        else:
            print(out_bytes.decode())
            ok = True

if __name__ == "__main__":
    main()
