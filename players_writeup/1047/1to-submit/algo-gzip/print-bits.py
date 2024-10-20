import os, sys

path = sys.argv[1]
with open(path, 'rb') as f:
	for b in f.read():
		for i in range(0, 8, +1):
			print(b>>i&1, end='')
	print()