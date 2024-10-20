import os
import re

os.chdir(os.path.dirname(__file__))

KEY_PATTERN = re.compile(r"\|0\|(.)(.)(.)(.)(.)(.)(.)(.)\|")
output_bytes = bytearray()

with open("tas1.fm2", "r", -1, "utf8") as reader:
  lines = reader.read().splitlines()

for line in lines:
  if not line.startswith("|"):
    continue

  right, left, down, up, start, select, b, a = KEY_PATTERN.match(line).groups()
  byte = 0
  for key in (right, left, down, up, start, select, b, a):
    if key != ".":
      byte |= 1
    byte <<= 1

  byte >>= 1
  output_bytes.append(byte)

for i in range(20):
  output_bytes.append(0)

with open("tas1.bin", "wb") as writer:
  writer.write(output_bytes[1:5000])
