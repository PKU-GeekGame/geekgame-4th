level=int(input("Level: "))
assert level in [1,2,3]
expr=input("Enter your expression: ")
assert len(expr)<50
assert len(set(expr)-set('n+-*/%()0123456789'))==0
fun=eval(f'lambda n: {expr}', {}, {})
if level==1:
    primes=list(range(2,500))
    for j in primes[:]:
        primes=[i for i in primes if i<=j or i%j!=0]
    for i in range(2,500):
        assert fun(i)==int(i in primes)
else:
    a,b=0,1
    maxn=200 if level==3 else 40
    for n in range(1,maxn):
        res=fun(n)
        assert res==a
        if level==3:
            assert isinstance(res,int)
        a,b=b,a+2*b
print(open(f"flag{level}.txt").read())