primes=list(range(2,5000))
for j in primes[:]:
    primes=[i for i in primes if i<=j or i%j!=0]
   
for a in primes:
    for b in primes:
        if a == b: break
        fail = False
        expr = lambda n: 0**(((a**(n-1)%n)*(b**(n-1)%n)-1)%100000)
        for i in range(2, 500):
            if expr(i) != int(i in primes):
                fail = True
                break
        if not fail:
            print(a, b)
            break
