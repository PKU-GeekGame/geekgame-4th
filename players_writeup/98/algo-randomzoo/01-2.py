import os

os.chdir(os.path.dirname(__file__))

diff_list = [[] for _ in range(0x100)]

for t in range(0x10):
  reader = open(f"task1-{t:02d}.txt", "r", -1, "utf8")
  lines = reader.read().splitlines()
  ints = [int(line) for line in lines if line]
  for i, value in enumerate(ints):
    if i < 31:
      continue

    diff = (ints[i - 31] + ints[i - 3]) % 2147483648 - ints[i]
    diff_list[i].append(diff)

with open("diff.txt", "w", -1, "utf8", None, "\n") as writer:
  for i, diffs in enumerate(diff_list):
    if not diffs:
      continue
    writer.write(f"{i}\t{max(diffs)}\n")
    writer.flush()
