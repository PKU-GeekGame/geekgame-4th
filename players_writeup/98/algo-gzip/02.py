import random
import gzip

from helper import byte_to_bits, bits_to_byte, CHARACTERS, HUFFMAN_TREE


欢愉 = b"\x17[What can I say? Mamba out! --KobeBryant]"
header = ""

bit_array = []

for byte in 欢愉:
  bits = byte_to_bits(byte)
  bit_array.extend(bits)

for i in range(5, len(bit_array), 6):
  bits = bit_array[i : i + 6]
  byte = bits_to_byte(bits)
  header += chr(HUFFMAN_TREE[str(byte)] ^ 27)


body = ""
char_counts = [header.count(_) for _ in CHARACTERS]
for char, count in zip(CHARACTERS, char_counts):
  body += char * (4 - count)

body = list(body)
random.seed(114514)
random.shuffle(body)
text_after = header + "".join(body)

text_len = len(text_after)
after = list(range(text_len))
random.seed("12345")
random.shuffle(after)

text_before = [0 for _ in range(text_len)]
for i, j in enumerate(after):
  text_before[j] = text_after[i]

text = [ord(c) ^ 27 for c in text_before]
random.seed("12345")
random.shuffle(text)

text = gzip.compress(bytes(text))

print("Before processing:")
print("".join(text_before))
print("After processing:")
print(text)
