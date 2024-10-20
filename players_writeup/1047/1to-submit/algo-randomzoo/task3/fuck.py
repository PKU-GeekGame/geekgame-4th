import sys 

outputs = [int(input()) for _ in range(65536)]

def get_all_posible_lengths():
	for flag_len in range(20, 100):
		failed = False
		max_max_delta = 0
		for a_base in range(607, 607+flag_len):
			def f(base):
				return (outputs[base] - outputs[base-607] - outputs[base-273])%(1<<31)
			deltas = []
			for base in range(a_base, 30000, flag_len):
				deltas.append(f(base))
			max_delta = 0
			for x in deltas:
				max_delta = max(max_delta, min((x-deltas[0])%(1<<31), (deltas[0]-x)%(1<<31)))
			max_max_delta = max(max_max_delta, max_delta)
		if max_max_delta == 1:
			print('flag length:', flag_len)

# get_all_posible_lengths()
# sys.exit(0)

# for flag_len in range(53, 54):
# 	ok = True
# 	checked = False
# 	for i in range(607, 65536):
# 		def is_legal(c):
# 			return c <= 130
# 		p0 = i - 607
# 		p1 = i - 273
# 		c0 = corresp_char(p0, flag_len)
# 		c1 = corresp_char(p1, flag_len)
# 		c2 = corresp_char(i, flag_len)
# 		if c0 and c2:
# 			checked = True
# 			rand0 = outputs[p0] - c0
# 			rand2 = outputs[i] - c2
# 			c1 = (rand0+outputs[p1]-rand2)%(1<<31)
# 			if not is_legal(c1):
# 				ok = False
# 				break
# 		elif c0 and c1:
# 			checked = True
# 			rand0 = outputs[p0] - c0
# 			rand1 = outputs[p1] - c1
# 			c2 = (outputs[i] - rand0 - rand1)%(1<<31)
# 			if not is_legal(c2):
# 				ok = False
# 				break
# 		elif c1 and c2:
# 			checked = True
# 			rand1 = outputs[p1] - c1
# 			rand2 = outputs[i] - c2
# 			c0 = (rand1+outputs[p0]-rand2)%(1<<31)
# 			if not is_legal(c0):
# 				ok = False
# 				break
# 	if not checked:
# 		print('WARN Never checked:', flag_len)
# 	else:
# 		if ok:
# 			print('OK:', flag_len)
# 		else:
# 			print('NOT OK:', flag_len)

FLAG_LEN = 53

def print_mod_info(n):
	print(f"{n}, {n%FLAG_LEN}, {FLAG_LEN-n%FLAG_LEN}")

print_mod_info(607)
print_mod_info(273)
print_mod_info(334)

import numpy as np

A = np.zeros((FLAG_LEN, FLAG_LEN), dtype=np.float32)
b = np.zeros(FLAG_LEN, dtype=np.float32)

for flag_base in range(0, FLAG_LEN):
	deltas = []
	for base in range(607+flag_base, 65536, FLAG_LEN):
		a0 = outputs[base-607]
		a1 = outputs[base-273]
		a2 = outputs[base]
		d = (a0+a1-a2)%(1<<31)
		deltas.append(d)
	# print(set(deltas))
	real_delta = max(deltas)
	flag_pos0 = (flag_base)%FLAG_LEN
	flag_pos1 = (607+flag_base-273)%FLAG_LEN
	flag_pos2 = (607+flag_base)%FLAG_LEN
	A[flag_base][flag_pos0] = 1
	A[flag_base][flag_pos1] = 1
	A[flag_base][flag_pos2] = -1
	b[flag_base] = real_delta

x = np.linalg.solve(A, b)
print(x)

flag = ''
for elem in x:
	flag += chr(int(elem))
print(flag)
