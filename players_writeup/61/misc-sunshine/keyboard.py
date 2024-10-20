with open("sunshine.log", "r") as f:
	s = f.readlines()

qmap = {
	13: "RET",
	116: "F5",
	161: "RSHIFT",
	191: "?",
	160: "LSHIFT",
}

for i, line in enumerate(s):
	if (line == "keyAction [00000003]\n"):
		c = int(s[i + 1][9:13],16)-0x8000
		if c >= 32 and c <= 90:
			print(chr(c), end="")
		elif c in qmap:
			print(f" [{qmap[c]}] ", end="")
		else:
			print(f" unknown {c} ", end="")