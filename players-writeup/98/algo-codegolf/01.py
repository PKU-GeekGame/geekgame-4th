expr = "0**(509**(n-1)%n-1)*0**(503**(n-1)%n-1)"
assert len(set(expr) - set("n+-*/%()0123456789")) == 0
fun = eval(f"lambda n: {expr}", {}, {})

primes = list(range(2, 500))
for j in primes[:]:
  primes = [i for i in primes if i <= j or i % j != 0]

for i in range(2, 500):
  if fun(i) != int(i in primes):
    print(i, fun(i), int(i in primes))
