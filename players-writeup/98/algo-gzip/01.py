import gzip
import random

from helper import average_bit_count, CHARACTERS, HUFFMAN_TREE

seed = 0
while True:
  虚无 = [0, 1, 2, 4, 8, 16, 32, 3, 5, 6, 9, 10, 12, 17, 18, 20, 24, 33, 34, 36, 40, 48, 7, 11, 13] * 13
  random.seed(seed)
  random.shuffle(虚无)

  header = ""
  bit_array = []

  for byte in 虚无:
    header += chr(HUFFMAN_TREE[str(byte)] ^ 27)

  body = ""
  char_counts = [header.count(_) for _ in CHARACTERS]
  max_charcount = max(char_counts)
  print(max_charcount)
  for char, count in zip(CHARACTERS, char_counts):
    body += char * (15 - count)

  body = list(body)
  random.seed(114514)
  random.shuffle(body)
  text_after = "".join(header) + "".join(body)

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
  prefix = (text + b"\xff" * 256)[:256]
  print("Prefix:")
  print(prefix)
  print(average_bit_count(prefix))

  if average_bit_count(prefix) < 2.49:
    break

  seed += 1
