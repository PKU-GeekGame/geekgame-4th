import random
from itertools import combinations
import os

from subprocess import check_output, STDOUT, PIPE


def spfa():
    '''
    https://zh.wikipedia.org/wiki/%E6%9C%80%E7%9F%AD%E8%B7%AF%E5%BE%84%E5%BF%AB%E9%80%9F%E7%AE%97%E6%B3%95

    https://www.cnblogs.com/luckyblock/p/14317096.html
    n: vertex
    m: edge
    w: weight
    '''
    n = 2000
    p_max = 40
    q_max = 50
    m = 3 * (p_max - 1) * (q_max - 1)

    output = ''
    m_counter = 0

    for ip in range(p_max - 1):
        for iq in range(q_max - 1):
            idx = 1 + ip * q_max + iq
            assert idx <= n
            output += f"{idx} {idx + 1} {random.randint(0, 500000) + 100} "
            output += f"{idx} {idx + q_max + 1} {random.randint(0, 500000) + 100} "
            # output += f"{idx + 1} {idx + q_max} {random.randint(0, 100) + 200000} "
            output += f"{idx} {idx + q_max} {random.randint(1, 1) + 1} "
            m_counter += 4

    output = f"{n} {m} {1} {n} " + output
    return output


def run_spfa():
    resp = 0
    while resp < 2e6:
        spfa_in = spfa()
        with open('spfa_in', 'w') as fp:
            fp.write(spfa_in)

        resp = int(check_output('cat spfa_in | ./spfa 1>/dev/null', shell=True, stderr=STDOUT).decode().strip())

    print(resp)
    # flag{YoU_kN0w_th3_DE@tH_Of_Spfa}

def gen_dinic():
    '''https://www.zhihu.com/question/266149721/answer/303649655
    '''

    maxn  = 100
    maxm  = 5000

    npath = 16
    n_bi = maxn - 2*npath
    bi_sides_st = 2*npath + 1
    bi_sides_ed = 2*npath + 1 + n_bi // 2


    output = ''
    krand_low = 33
    krand_up = 33

    infrand_low = 20000
    infrand_up = 30000


    # bi-sides
    for bi_st in range(bi_sides_st + 1, bi_sides_ed):
        for bi_ed in range(bi_sides_ed + 1, maxn):
            output += f"{bi_st} {bi_ed} {random.randint(0, 0) + 1} "
    
    # add path-bisides
    for i in range(1, npath + 1, 2):
        if i % 4 == 1:
            for bi_st in range(bi_sides_st + 1, bi_sides_ed):
                output += f"{i} {bi_st} {random.randint(0, krand_up) + krand_low} "
        else:
            for bi_ed in range(bi_sides_ed + 1, maxn):
                output += f"{i} {bi_ed} {random.randint(0, krand_up) + krand_low} "

    
    for i in range(npath + 2, 2*npath + 1, 2):
        if i % 4 == 2:
            for bi_st in range(bi_sides_st + 1, bi_sides_ed):
                output += f"{bi_st} {i} {random.randint(0, krand_up) + krand_low} "
        else:
            for bi_ed in range(bi_sides_ed + 1, maxn):
                output += f"{bi_ed} {i} {random.randint(0, krand_up) + krand_low} "
    
    # single path
    for i in range(1, 2*npath + 1):
        output += f"{i} {i+1} {random.randint(0, infrand_up) + infrand_low} "


    print(f"curr_m: {len(output.strip().split(' ')) // 3}")
    # print(f'curr_w: {[ for i in range(2, len(output), 3)]}')

    output = f"{maxn} {len(output.strip().split(' ')) // 3} {1} {2*npath} " + output

    return output


def run_dinic(loop=False):
    resp = 0
    while resp < 1e6:
        dinic_in = gen_dinic()
        with open('dinic_in', 'w') as fp:
            fp.write(dinic_in)

        resp = int(check_output('cat dinic_in | ./dinic 1>/dev/null', shell=True, stderr=STDOUT).decode().strip())

        if not loop:
            break

    print(resp)

# flag{y0U_coMPlEtE1y_uNd3rSt4Nd_tH3_D1Nic_AlgOr1THM}
run_dinic(loop=True)