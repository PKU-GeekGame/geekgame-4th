truth = [0, 1]

for i in range(2, 40):
    truth.append(truth[i-1] * 2 + truth[i-2])

print(truth)

# f = lambda n: (13860**n+8119*5741**(n-1))//(2*8119*5741**(n-1))
f = lambda n: (93222358**n//(54608393*38613965**(n-1))+1)//2
# f = lambda n: (225058681**(n+1)//(131836323*93222358**n)+1)//2

seq = [0] + [f(n) for n in range(1, 40)]
print(seq)
print(list(i for i in range(1, 40) if seq[i] != truth[i]))

# f = lambda n: ((3**(n+1)+1)**(n-1)%(9**(n+1)-2))%(3**(n+1)-1)
# f = lambda n: (3**n+1)**(n-1)//(3**n+1)%(9**n-2)%(3**n-1)
