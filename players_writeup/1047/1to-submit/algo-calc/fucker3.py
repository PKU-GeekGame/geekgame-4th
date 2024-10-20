import math, os, sys

k = 196
s = 3**k
m = s**2-2
assert s*s%m == 2
assert math.gcd(s, m) == 1
assert math.gcd(2, m) == 1
s_inv = s*(s+1)//2-1
assert s*s_inv%m == 1

r = (s+1)//2
assert r%2 == 1
assert (r*m+1)%(2*s) == 0

s2_inv = (3**k*r-1) // 2
assert (2*s) * (s2_inv) %m == 1

# aa = 577
# bb = 408
expr = f"(1+3**196)**(n-1)%(3**392-2)//3**196"
# expr = f"((1+s)**(n-1)-(1-s)**(n-1)) % m//2//s"
print("Expr len:", len(expr))
fun = "lambda n: " + expr
fun = eval(fun)

maxn=200

a,b=0,1
for n in range(1,200):
    res=fun(n)
    print("%2d"%n, res, a)
    a,b=b,a+2*b

a,b=0,1
for n in range(1,maxn):
    res=fun(n)
    if res != a:
        print(n, res, a)
        assert False
    assert res==a
    a,b=b,a+2*b

print("PASS")