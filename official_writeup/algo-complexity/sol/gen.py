import random

edge = []
n = 10
m = 200
for i in range(n):
    for j in range(m):
        if j < m - 1:
            edge.append((i * m + j, i * m + j + 1, 100 + (-1) ** j * i * 3))
            # edge.append((i * m + j + 1, i * m + j, 100 + (-1) ** j * i * 3))
            # edge.append((i * m + j, i * m + j + 1, random.randint(10, 100)))
            # # edge.append((i * m + j + 1, i * m + j, random.randint(10, 100)))
            # if i < n - 1:
            #     edge.append((i * m + j, (i + 1) * m + j + 1, random.randint(10, 100)))
            #     # edge.append(((i + 1) * m + j + 1, i * m + j, random.randint(10, 100)))
        if i < n - 1:
            edge.append((i * m + j, (i + 1) * m + j, 1))
            # edge.append(((i + 1) * m + j, i * m + j, 1))
print(n * m, len(edge))
with open("spfa.txt", "w") as f:
    print(n * m, len(edge), "1", n * m, file=f)
    for u, v, w in edge:
        print(u + 1, v + 1, w, file=f)

edge = []
n = 100
k = n // 3
p = n // 12 - 1
s = 1
t = k * 2 + p * 4 + 2
for i in range(k):
    edge.append((s, i + 2, k))
    edge.append((k + 2 + i, t, k))

for i in range(k):
    for j in range(k):
        edge.append((i + 2, k + j + 2, 1))

edge.append((s, k * 2 + 2, k * k * p))
edge.append((k * 2 + 2, k * 2 + 3, k * k * p))
edge.append((k * 2 + 2 + p * 2, t, k * k * p))
edge.append((k * 2 + 3 + p * 2, k * 2 + 2 + p * 2, k * k * p))
for i in range(k):
    edge.append((k * 2 + 3, k + 2 + i, k))
    edge.append((i + 2, k * 2 + 3 + p * 2, k))

for j in range(1, p):

    edge.append((k * 2 + 1 + j * 2, k * 2 + 2 + j * 2, k * k * p))
    edge.append((k * 2 + 2 + j * 2, k * 2 + 3 + j * 2, k * k * p))
    edge.append((k * 2 + 2 + p * 2 + j * 2, k * 2 + 1 + p * 2 + j * 2, k * k * p))
    edge.append((k * 2 + 3 + p * 2 + j * 2, k * 2 + 2 + p * 2 + j * 2, k * k * p))
    if j & 1:
        for i in range(k):
            edge.append((k * 2 + 3 + j * 2, 2 + i, k))
            edge.append((k + i + 2, k * 2 + 3 + p * 2 + j * 2, k))
    else:
        for i in range(k):
            edge.append((k * 2 + 3 + j * 2, k + 2 + i, k))
            edge.append((i + 2, k * 2 + 3 + p * 2 + j * 2, k))

print(t, len(edge))
with open("dinic.txt", "w") as f:
    print(t, len(edge), s, t, file=f)
    for u, v, w in edge:
        print(u, v, w, file=f)
