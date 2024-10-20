from pwn import *
p = process(['nc', 'prob16.geekgame.pku.edu.cn', '10016'])
print(p.recvuntil(b'input your token: ').decode(), end='')
p.sendline(b'... my token ...')

def reverse_right(x, bit, mask=0xffffffff):
    tmp = x 
    for _ in range(32 // bit):
        tmp = x ^ ((tmp >> bit) & mask)
    return tmp

def reverse_left(x, bit, mask=0xffffffff):
    tmp = x 
    for _ in range(32 // bit):
        tmp = x ^ ((tmp << bit) & mask)
    return tmp

def reverse_extract_number(m):
    m=reverse_right(m, 18)
    m=reverse_left(m, 15, 4022730752)
    m=reverse_left(m, 7, 2636928640)
    m=reverse_right(m, 11)
    return m & 0xffffffff

def _int32(x):
    return int(0xFFFFFFFF & x)

def extract_number(y):
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & 2636928640)
    y = y ^ ((y << 15) & 4022730752)
    y = y ^ (y >> 18)
    return _int32(y)

num_list = []
for _ in range(624 * 2):
    i = int(p.recvline().decode())
    num_list.append(i)
    p.sendline(b'')

# print(num_list)

# 第一个返回值代表是否解出，第二个代表当前 flag_len 是否可能成立，第三个为实际解出结果
def solve(solved):
    is_real_flag_len = True
    while True:
        changed = False
        for i in range(flag_len):
            i0 = i % flag_len
            i1 = (i + 1) % flag_len
            i397 = (i + 397) % flag_len
            i624 = (i + 624) % flag_len
            if solved[i1] >= 0 and solved[i397] >= 0:
                if solved[i624] == -1:
                    # print(1)
                    n1 = reverse_extract_number(num_list[i + 1] - solved[i1])
                    n397 = reverse_extract_number(num_list[i + 397] - solved[i397])
                    res = (n1 & 0x7FFFFFFF) >> 1
                    res = res ^ n397
                    if n1 % 2 != 0:
                        res = res ^ 0x9908B0DF
                    possible1 = extract_number(res)
                    possible2 = extract_number(res ^ 0x40000000)
                    real1 = 0x0 <= num_list[i + 624] - possible1 <= 0x7F
                    real2 = 0x0 <= num_list[i + 624] - possible2 <= 0x7F
                    if real1 and real2:
                        print(flag_len, 'this flag len can have multiple answers')
                    elif real1:
                        solved[i624] = num_list[i + 624] - possible1
                    elif real2:
                        solved[i624] = num_list[i + 624] - possible2
                    else:
                        is_real_flag_len = False
                        break
                    changed = True
            elif solved[i397] >= 0 and solved[i624] >= 0:
                if solved[i1] == -1:
                    # print(2)
                    n397 = reverse_extract_number(num_list[i + 397] - solved[i397])
                    n624 = reverse_extract_number(num_list[i + 624] - solved[i624])
                    res = n397 ^ n624
                    if (res & 0x80000000) == 0x80000000:
                        res = res ^ 0x9908B0DF
                        res = (res << 1) + 1
                    else:
                        res = res << 1

                    possible1 = extract_number(res)
                    possible2 = extract_number(res ^ 0x80000000)
                    real1 = 0x0 <= num_list[i + 1] - possible1 <= 0x7F
                    real2 = 0x0 <= num_list[i + 1] - possible2 <= 0x7F
                    if real1 and real2:
                        print(flag_len, 'this flag len can have multiple answers')
                    elif real1:
                        solved[i1] = num_list[i + 1] - possible1
                    elif real2:
                        solved[i1] = num_list[i + 1] - possible2
                    else:
                        is_real_flag_len = False
                        break
                    changed = True
            elif solved[i1] >= 0 and solved[i624] >= 0:
                if solved[i397] == -1:                    
                    n1 = reverse_extract_number(num_list[i + 1] - solved[i1])
                    n624 = reverse_extract_number(num_list[i + 624] - solved[i624])
                    res = (n1 & 0x7FFFFFFF) >> 1
                    res = res ^ n624
                    if n1 % 2 != 0:
                        res = res ^ 0x9908B0DF
                    possible1 = extract_number(res)
                    possible2 = extract_number(res ^ 0x40000000)
                    real1 = 0x0 <= num_list[i + 397] - possible1 <= 0x7F
                    real2 = 0x0 <= num_list[i + 397] - possible2 <= 0x7F
                    if real1 and real2:
                        print(flag_len, 'this flag len can have multiple answers')
                    elif real1:
                        solved[i397] = num_list[i + 397] - possible1
                    elif real2:
                        solved[i397] = num_list[i + 397] - possible2
                    else:
                        is_real_flag_len = False
                        break
                    changed = True
        if not is_real_flag_len or not changed:
            break
    if not is_real_flag_len:
        return False, False, solved
    for i in solved:
        if i == -1:
            return False, True, solved
    return True, True, solved

def get_initial_flag(flag_len):
    # return [ord('f'), ord('l'), ord('a'), ord('g'), ord('{')] + [0] * (flag_len - 6) + [ord('}')]
    return [ord('f'), ord('l'), ord('a'), ord('g'), ord('{')] + [-1] * (flag_len - 5)

def get_initial_flag_01(flag_len):
    return [1] * 5 + [0] * (flag_len - 5)

def print_flag(solved):
    print(solved)
    for i in solved:
        print(chr(i), end='')
    print()

# 这个函数用来枚举得到最好的添加信息的位置（在某些位置添加信息可能能得到所有值，但某些位置不行）
def find_best_enumerate_pos_1(flag_len):
    best_res = []
    best_a = 0
    for a in range(5, flag_len - 1):
        # solved = [1] * 5 + [0] * (flag_len - 6) + [1]
        solved = get_initial_flag_01(flag_len)
        solved[a] = 1
        while True:
            changed = False
            for i in range(flag_len):
                i0 = i % flag_len
                i1 = (i + 1) % flag_len
                i397 = (i + 397) % flag_len
                i624 = (i + 624) % flag_len
                if solved[i1] and solved[i397]:
                    if not solved[i624]:
                        solved[i624] = 1
                        changed = True
                elif solved[i397] and solved[i624]:
                    if not solved[i1]:
                        solved[i1] = 1
                        changed = True
                elif solved[i1] and solved[i624]:
                    if not solved[i397]:
                        solved[i397] = 1
                        changed = True
            if not changed:
                break
        if solved.count(1) > best_res.count(1):
            best_res = solved
            best_a = a
    return best_res.count(1), best_a

def find_best_enumerate_pos_2(flag_len):
    best_res = []
    best_a = 0
    best_b = 0
    for a in range(5, flag_len - 1):
        for b in range(a + 1, flag_len - 1):
            # solved = [1] * 5 + [0] * (flag_len - 6) + [1]
            solved = get_initial_flag_01(flag_len)
            solved[a] = 1
            solved[b] = 1
            while True:
                changed = False
                for i in range(flag_len):
                    i0 = i % flag_len
                    i1 = (i + 1) % flag_len
                    i397 = (i + 397) % flag_len
                    i624 = (i + 624) % flag_len
                    if solved[i1] and solved[i397]:
                        if not solved[i624]:
                            solved[i624] = 1
                            changed = True
                    elif solved[i397] and solved[i624]:
                        if not solved[i1]:
                            solved[i1] = 1
                            changed = True
                    elif solved[i1] and solved[i624]:
                        if not solved[i397]:
                            solved[i397] = 1
                            changed = True
                if not changed:
                    break
            if solved.count(1) > best_res.count(1):
                best_res = solved
                best_a = a
                best_b = b
    return best_res.count(1), best_a, best_b

def find_best_enumerate_pos_3(flag_len):
    best_res = []
    best_a = 0
    best_b = 0
    best_c = 0
    for a in range(5, flag_len - 1):
        for b in range(a + 1, flag_len - 1):
            for c in range(b + 1, flag_len - 1):
                # solved = [1] * 5 + [0] * (flag_len - 6) + [1]
                solved = get_initial_flag_01(flag_len)
                solved[a] = 1
                solved[b] = 1
                solved[c] = 1
                while True:
                    changed = False
                    for i in range(flag_len):
                        i0 = i % flag_len
                        i1 = (i + 1) % flag_len
                        i397 = (i + 397) % flag_len
                        i624 = (i + 624) % flag_len
                        if solved[i1] and solved[i397]:
                            if not solved[i624]:
                                solved[i624] = 1
                                changed = True
                        elif solved[i397] and solved[i624]:
                            if not solved[i1]:
                                solved[i1] = 1
                                changed = True
                        elif solved[i1] and solved[i624]:
                            if not solved[i397]:
                                solved[i397] = 1
                                changed = True
                    if not changed:
                        break
                if solved.count(1) > best_res.count(1):
                    best_res = solved
                    best_a = a
                    best_b = b
                    best_c = c
    return best_res.count(1), best_a, best_b, best_c

# 枚举 flag 的长度
for flag_len in range(10, 70):
    print(flag_len)
    solved = get_initial_flag(flag_len)
    result, flag_len_ok, solved = solve(solved)
    if result:
        print_flag(solved)
        break
    if not flag_len_ok:
        continue
    best_res, best_a = find_best_enumerate_pos_1(flag_len)
    if best_res == flag_len:
        really_solved = False
        for i in range(0x0, 0x80):  # 枚举
            solved = get_initial_flag(flag_len)
            solved[best_a] = i
            result, flag_len_ok, solved = solve(solved)
            if result:
                print_flag(solved)
                really_solved = True
                break
        if really_solved:
            break
        continue
    # continue
    # 答案的长度居然只有 30，根本不需要后面的代码，被 \n 坑了
    best_res, best_a, best_b = find_best_enumerate_pos_2(flag_len)
    if best_res == flag_len:
        really_solved = False
        for i in range(0x0, 0x80):
            for j in range(0x0, 0x80):
                solved = get_initial_flag(flag_len)
                solved[best_a] = i
                solved[best_b] = j
                result, flag_len_ok, solved = solve(solved)
                if result:
                    print_flag(solved)
                    really_solved = True
                    break
            if really_solved:
                break
        if really_solved:
            break
        continue
    best_res, best_a, best_b, best_c = find_best_enumerate_pos_3(flag_len)
    print(best_res, best_a, best_b, best_c)
    assert(best_res == flag_len)
    really_solved = False
    for i in range(0x0, 0x80):
        for j in range(0x0, 0x80):
            for k in range(0x0, 0x80):
                solved = get_initial_flag(flag_len)
                solved[best_a] = i
                solved[best_b] = j
                solved[best_c] = k
                result, flag_len_ok, solved = solve(solved)
                if result:
                    print_flag(solved)
                    really_solved = True
                    break
            if really_solved:
                break
        if really_solved:
            break
    if really_solved:
        break