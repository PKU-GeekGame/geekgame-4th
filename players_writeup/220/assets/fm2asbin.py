#!/usr/bin/env python3

import re


BUTTONS = ['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']


def fm2_to_bin(d: str) -> bytes:
  res = bytearray()
  for l in d.splitlines():
    if not l.startswith('|'):
      continue
    byte = 0
    for (i, c) in enumerate(BUTTONS):
      if c in l:
        byte |= 1 << i
    res.append(byte)
  return res[1:]




if __name__ == '__main__':
  import sys
  with open(sys.argv[1], 'r') as f:
    fm2 = f.read()
  with open(sys.argv[2], 'wb') as f:
    f.write(fm2_to_bin(fm2))
