expr = "((1+2**(1/2))**(n-1)+1)/2**(1/2)//2"
print("Expr len:", len(expr))
fun = "lambda n: " + expr
fun = eval(fun)

for n in range(10):
    print(fun(n))

a,b=0,1
maxn=40
for n in range(1,maxn):
    res=fun(n)
    if res != a:
        print(n, res, a)
        assert False
    assert res==a
    a,b=b,a+2*b

