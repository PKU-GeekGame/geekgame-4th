import random, os, sys, gzip

random.seed(12345)

TREE_SIZE = 63

## TREE_SIZE Normal CHARACTER
## <END 256> <DUP3 257> Merge First

CYCLE_TIME = 10
TOTAL_LEN = TREE_SIZE * CYCLE_TIME
DUP_TIME = CYCLE_TIME - 4
## DUP 3: A bit Smaller than Normal CHARACTER freq.

charset = [i ^ 30 for i in range(0x20, 0x7f)]
random.shuffle(charset)
charset = charset[:TREE_SIZE]
charset.sort()

s = bytes()
A = set()

## 256 for end mark

def append(c):
	global A, s
	if len(s) >= 2:
		A.add(s[-2:] + bytes([c]))
	s += bytes([c])

def insert_c():
	global s, r, A
	fail = []
	for _ in range(len(r)):
		c = r[0]
		wd = s[-2:] + bytes([c])
		if len(s) <= 2 or not (wd in A):
			append(c)
			r = r[1:] + [c]
			break
		else:
			r = r[1:]
			fail = fail + [c]
	else:
		assert(0)
	r = fail + r

with open("inject.txt", "r") as f:
	stream = ''.join(list(map(lambda x: x[::-1], f.read().split())))

for i in range(0, len(stream), 6):
	code = stream[i : i + 6]
	assert(code != "111111")
	append(charset[int(code, 2)])

r = charset.copy()
while len(s) < TOTAL_LEN:
	insert_c()

for i in range(DUP_TIME):
	x = random.randint(0, len(s)-3)
	s = s + s[x : x + 3]

sys.stdout.buffer.write(s)
payload = s

with open("answer2.txt", "w") as of:
	_output = [chr(c ^ 30) for c in payload]
	order = [i for i in range(len(payload))]
	random.seed('114514')
	random.shuffle(order)
	output = [''] * len(payload)
	for i in range(len(payload)):
		output[order[i]] = _output[i]
	of.write("".join(output))
