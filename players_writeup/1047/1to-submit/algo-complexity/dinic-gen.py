import random
random.seed(0)

n = 100
edges = []
MX = 10000
for i in range(1, n-1):
	edges.append((i, i+1, MX))
	edges.append((i+1, n, 1))
edges.append((n-1, n, MX))

while len(edges) < 5000:
	a = random.randint(1, n)
	b = random.randint(1, n)
	if a == b:
		continue
	edges.append((a, b, random.randint(1, 2)))

m = len(edges)
print(n, m, 1, n)
for e in edges:
	print(*e)
	