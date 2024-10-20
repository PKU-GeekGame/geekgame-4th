import random
fp = open("spfa.in", "w")
N = 2000
M = 8000
W = 9.99e8

# rectanglar grid
a = 4
b = N // a
n = a * b
s = 1
t = n

edges = []
for i in range(a):
    for j in range(b):
        u = i * b + j + 1
        if i > 0:
            v = (i - 1) * b + j + 1
            w = 1
            edges.append((u, v, w))
            if j > 0:
                v = (i - 1) * b + j
                w = random.randint(200, 500) + 100
                edges.append((u, v, w))
        if j > 0:
            v = i * b + j
            w = random.randint(200, 500) + 100
            edges.append((u, v, w)) 
random.shuffle(edges)
m = len(edges)

sumw = 0
for i in range(m):
    sumw += edges[i][2]

assert sumw <= W
assert m <= M
assert n <= N

print(n, m, s, t, sumw)

print(n, m, s, t, file=fp)
for u, v, w in edges:
    print(u, v, w, file=fp)
fp.close()