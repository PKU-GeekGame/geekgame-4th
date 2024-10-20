from cyaron import *
import os
K = int(os.getenv("K_VAL", 10))
io = IO("dinic.in")
g = Graph(100, directed=True)
a = 1
bin_a = range(2, 2 + K)
ext_a = range(2 + K, 51)
bin_b = range(51, 51 + K)
ext_b = range(51 + K, 100)
b = 100
MAX = 100000

for v in bin_a:
    g.add_edge(a, v, weight=K)
for u in bin_b:
    g.add_edge(u, b, weight=K)
for u in bin_a:
    for v in bin_b:
        g.add_edge(u, v, weight=1)


g.add_edge(a, ext_a[0], weight=MAX)
g.add_edge(ext_b[-1], b, weight=MAX)

for u in ext_a:
    g.add_edge(u - 1, u, weight=MAX)
for u in ext_b:
    g.add_edge(u, u + 1, weight=MAX)


for u in ext_a:
    if u % 2 == 0:
        if u % 4 == 0:
            for v in bin_b:
                g.add_edge(u, v, weight=K)
        else:
            for v in bin_a:
                g.add_edge(u, v, weight=K)

for v in ext_b:
    if v % 2 == 0:
        if v % 4 != 0:
            for u in bin_a:
                g.add_edge(u, v, weight=K)
        else:
            for u in bin_b:
                g.add_edge(u, v, weight=K)

io.input_writeln(100, g.edge_count(), 1, 100)
io.input_writeln(g.to_str())
