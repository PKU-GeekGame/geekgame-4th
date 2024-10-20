import os
import random

os.chdir(os.path.dirname(__file__))


class Edge:
  def __init__(self, start, end, weight):
    self.start = start
    self.end = end
    self.weight = weight


random.seed(114514)
n, m = 20, 100

v: list[Edge] = []

for i in range(1, n + 1):
  for j in range(1, m + 1):
    if j != m:
      v.append(Edge((i - 1) * m + j, (i - 1) * m + j + 1, random.randint(1, 100000)))
      v.append(Edge((i - 1) * m + j + 1, (i - 1) * m + j, random.randint(1, 100000)))
    if i != n:
      v.append(Edge((i - 1) * m + j, i * m + j, 1))
      v.append(Edge(i * m + j, (i - 1) * m + j, 1))

random.shuffle(v)

with open("01.txt", "w") as f:
  f.write(f"{n * m} {len(v)} 1 {n * m}\n")

  for edge in v:
    f.write(f"{edge.start} {edge.end} {edge.weight}\n")
