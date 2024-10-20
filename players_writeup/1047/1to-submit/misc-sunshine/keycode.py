lines = open('sunshine.log', 'r').readlines()
s = ""
next_action = 0
for line in lines:
	if 'keyAction' in line:
		next_action = int(line.strip().split()[1][1:-1])
	if 'keyCode' in line:
		keycode = line.strip().split()[1][1:-1]
		# print(next_action, keycode)
		if next_action == 3:
			input_char = int(keycode, 16)-0x8000
			mappings = {
				0x26: "UP",
				0x28: "DOWN",
				0x25: "LEFT",
				0x27: "RIGHT",
				0x20: " ",
				0x0D: "\n",
				0xa1: "SHIFT",
				0xbf: "/",
				0xBC: "<",
				0xA0: "SHIFT",
				0xDB: "{",
				0xDD: "}"
			}
			if 0x30 <= input_char <= 0x39:
				# 0-9
				s += chr(input_char-0x30+ord('0'))
			elif 0x41 <= input_char <= 0x5A:
				# A-Z
				s += chr(input_char-0x41+ord('A'))
			elif 0x60 <= input_char <= 0x69:
				# a-z
				s += chr(input_char-0x60+ord('0'))
			elif 0x70 <= input_char <= 0x87:
				# F1-F12
				s += "F" + str(input_char-0x70+1)
			else:
				if input_char in mappings:
					s += mappings[input_char]
					# print(mappings[input_char])
				else:
					print(hex(input_char))
			# s += '|'

print(s)
