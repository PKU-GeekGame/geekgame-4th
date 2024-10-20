import re


import sys

BUTTONS =['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']
with open(sys.argv[1], "r") as fm2:
	lines = fm2.readlines()
	output = b""
	for line in lines:
		if "|" in line:
			p = 0
			for i, button in enumerate(BUTTONS):
				if button in line:
					p |= 1 << i
			output += bytes([p])
	with open(sys.argv[2], "wb") as flag:
		flag.write(output[1:])