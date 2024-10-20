# https://www.cnblogs.com/luckyblock/p/14317096.html
# GPT 翻译成 python

import random
import time


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w


def r():
    return random.randint(0, (1 << 31) - 1)


# 初始化变量
v = []
n = 3
tp = 0
m = 2000 // n
id = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
a = [0] * 1000000

# 设置随机种子
random.seed(int(time.time()))

# 初始化 id 和 a 数组
for i in range(1, n + 1):
    for j in range(1, m + 1):
        tp += 1
        id[i][j] = tp
        a[tp] = tp

# 设置 SIZE
SIZE = 29989

# 构造边
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if i < n:
            v.append(Edge(id[i][j], id[i + 1][j], 1))
            v.append(Edge(id[i + 1][j], id[i][j], 1))
            if j < m:
                if True:
                    v.append(Edge(id[i][j], id[i + 1][j + 1], r() % SIZE + 10))
                else:
                    v.append(Edge(id[i + 1][j + 1], id[i][j], r() % SIZE + 10))
        if j < m:
            v.append(Edge(id[i][j], id[i][j + 1], r() % SIZE + 10))
            v.append(Edge(id[i][j + 1], id[i][j], r() % SIZE + 10))

# 打乱边的顺序
random.shuffle(v)

with open("flag1.txt", "w", encoding="utf-8") as f:
    f.write(f"{tp} {len(v)} 1 {tp}\n")
    for edge in v:
        f.write(f"{a[edge.u]} {a[edge.v]} {edge.w}\n")
