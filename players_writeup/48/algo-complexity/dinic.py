import random
N = 100
M = 5000
W = 10**9

fp = open("dinic.in", "w")
sumw = 0

p = 24
k = 25

s = 1
t = 2
n = 1 + 1 + 2 * p + 2 * k

def KL(i):
    return 2 + i

def KR(i):
    return 2 + k + i

def PL(i):
    return 2 + 2 * k + i

def PR(i):
    return 2 + 2 * k + p + i

edges = []
# 1. bipartite graph
for i in range(1, k + 1):
    for j in range(1, k + 1):
        edges.append((KL(i), KR(j), 1))
        sumw += 1
# 2. source to left
for i in range(1, k + 1):
    edges.append((s, KL(i), k))
    sumw += k
# 3. right to target
for i in range(1, k + 1):
    edges.append((KR(i), t, k))
    sumw += k
random.shuffle(edges)
# 4. L link to bi
for i in range(1, p + 1):
    for j in range(1, k + 1):
        edges.append((PL(i), KL(j), k))
        sumw += k
        edges.append((PL(i), KR(j), k))
        sumw += k
# 5. bi to R link
for i in range(1, p + 1):
    for j in range(1, k + 1):
        edges.append((KR(j), PR(i), k))
        sumw += k
        edges.append((KL(j), PR(i), k))
        sumw += k
# 6. Link
w0 = (W - sumw) // (2 * p + 1)
for i in range(1, p):
    edges.append((PL(i), PL(i + 1), w0))
    sumw += w0
    edges.append((PR(i), PR(i + 1), w0))
    sumw += w0
edges.append((PL(p), PR(1), w0))
sumw += w0
edges.append((s, PL(1), w0))
sumw += w0
edges.append((PR(p), t, w0))
sumw += w0

m = len(edges)

print(n, m, s, t, sumw)
print(n, m, s, t, file=fp)
assert sumw <= W
assert n <= N
assert m <= M
for u, v, w in edges:
    print(u, v, w, file=fp)
fp.close()