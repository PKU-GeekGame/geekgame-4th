# https://codeforces.com/blog/entry/104960

k = int(input())
# produces O(k) vertices and O(k^2) edges
# your implementation does \Omega(k^5) arc scans

inf = 100000
E = []
def add_edge(u, v, f):
    E.append((u, v, f))

V = 2
S = 0
T = 1 # note: is overwritten in last part

# first part: anti Edmonds-Karp test that generates O(V E) paths.
# build dense block
V += 2*k
left = lambda i : 2+i
right = lambda i : 2+k+i
for i in range(k):
    for j in range(k):
        add_edge(left(i), right(j), 1)

# build connections to alternating sides of block
A = S
B = T
for _ in range(k):
    add_edge(A, V, inf)
    add_edge(V, V+1, inf)
    A = V+1
    V+=2
    add_edge(V, B, inf)
    add_edge(V+1, V, inf)
    B = V+1
    V+=2
    for i in range(k):  
        add_edge(A, left(i), k)
        add_edge(right(i), B, k)
    # alternate sides
    left,right = right,left

# second part: another dense part that is visited for every path.
VV = V
V += 2*k
top = lambda i : VV+i
bottom = lambda i : VV+k+i
X = T
T = V
V += 1
# k^2 edges to be visited
for i in range(k):
    add_edge(S, top(i), k)
    add_edge(bottom(i), T, k)
    for j in range(k):
        add_edge(top(i), bottom(j), 1)
# relevant path through this part
add_edge(X, top(0), inf)
for i in range(k-1):
    add_edge(top(i), top(i+1), inf)
add_edge(top(k-1), T, inf)

print(V, len(E) * 7, S + 1, T + 1)
for u, v, w in E:
    for p in range(7):
    	print(u + 1, v + 1, w)