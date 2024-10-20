import os, sys

if __name__ == "__main__":
	if len(sys.argv) not in [3, 4]:
		print("Usage: %s <input> <output> [length-limit]" % sys.argv[0])
	
	with open(sys.argv[1], "r") as in_f:
		lines = in_f.readlines()
	while lines[0][0] != '|':
		lines.pop(0)
		
	lines.pop(0)

	length_limit = int(sys.argv[3]) if len(sys.argv) == 4 else 100000000000

	result = b''
	for line in lines:
		elems = line.strip().split('|')
		print(elems)
		assert elems[0] == ''
		assert elems[1] == '0'
		assert elems[3] == '........' or elems[3] == ''
		assert elems[4] == ''
		res = 0
		ops = elems[2]
		if 'A' in ops: res |= 1
		if 'B' in ops: res |= 2
		if 'S' in ops: res |= 4
		if 'T' in ops: res |= 8
		if 'U' in ops: res |= 16
		if 'D' in ops: res |= 32
		if 'L' in ops: res |= 64
		if 'R' in ops: res |= 128
		result += bytes([res])
		if len(result) >= length_limit:
			break
	
	with open(sys.argv[2], "wb") as out_f:
		out_f.write(result)
	