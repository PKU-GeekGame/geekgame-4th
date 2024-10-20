level = 2
expr = "(((1+2**(1/2))**(n-1))/8**(1/2)+1/2)//1"
fun = eval(f"lambda n: {expr}", {}, {})

a, b = 0, 1
maxn = 200 if level == 3 else 40
for n in range(1, maxn):
  res = fun(n)
  if res != a:
    print(n, res, a)

  if level == 3:
    assert isinstance(res, int)
  a, b = b, a + 2 * b
