from sympy import primerange

primes = set(primerange(1, 500))

def sieve(m):
    return set(n for n in range(1, 500) if m**n%n==m)

res = set(range(1, 500))

for i in [2,3]:
    s = sieve(i)
    print(len(s), s)
    res = res & s

print(res)
print(res - primes)
print(len(res - primes))
print(primes - res)

# alt = set(n for n in range(1,500) if (2**n+3**n-5)%n == 0)
# print(alt)
# print(primes-alt)
# print(alt-primes)

alt = set(n for n in range(1,500) if (2**n%n+3**n%n-5)*(n-2)*(n-3) == 0)
print(alt^primes)

f=lambda n: 1+(-((2**n%n+3**n%n-5)*(n-2)*(n-3))**2//99**99)
alt = set(n for n in range(1,500) if f(n) == 1)
print(alt^primes)
print(set(f(n) for n in range(1,500)))

a = list((2**n%n+3**n%n-5)*(n-2)*(n-3) for n in range(1,500))
a.sort()
print(a)

# print(sieve(2) & sieve(3) ^ set(n for n in range(1, 500) if 2**n%n+3**n%n==5))

# print([1+(-(2**n%n+3**n%n-5)**2*15852154868550%n)//99**99 for n in range(1, 2500)])

# s = [sieve(i) for i in range(20)]
# 
# for i in range(20):
#     for j in range(20):
#         if i >= j:
#             continue
#         sv = s[i] & s[j]
#         print(len(sv-primes), i, j)
