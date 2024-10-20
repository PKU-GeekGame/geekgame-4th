from math import *
a, b = 1, 2

for i in range(23):
	a, b = a * 2 + b, a
	
print(2)
print(f"({a}**n//{b}**(n-1)//{a+b}+1)//2")