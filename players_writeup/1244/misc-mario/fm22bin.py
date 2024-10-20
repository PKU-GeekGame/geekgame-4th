#!/usr/bin/env python3

# LSB to MSB, S is Select, T is Start
BUTTONS = ['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']
# S is Select, T is start
OTHER_BUTTONS_TEXT_ORDER = ['U', 'D', 'L', 'R', 'T', 'S', 'B', 'A']
OTHER_BUTTONS = ['A', 'B', 'T', 'S', 'U', 'D', 'L', 'R']
# Set to True for flag 2, False for flags 1 and 3
skip_first_frame = False

def fm2_to_bin(f) -> bytes:
  '''
  Converts the given FM2 file to binary data of per-frame input.
  '''
  global skip_first_frame
  buf = bytearray()
  for line in f:
    start_id = 0
    buttons_bits = BUTTONS
    if line.startswith("|    0,..|"):
      start_id = 10
      func = lambda x: 1 << x
      buttons_bits = OTHER_BUTTONS
    elif line.startswith('|0|'):
      start_id = 3
    else:
      continue
    if skip_first_frame:
      skip_first_frame = False
      continue
    buttons = line[start_id:start_id + 8]
    b = 0
    for i, button in enumerate(buttons_bits):
      if button in buttons:
        b |= (1 << i)
    buf.append(b)
  return bytes(buf)
  # For flag 3
  # bbuf = buf[26:59 + 162]
  # bbuf.extend(buf[383:4954:2])
  # bbuf.extend(buf[4954:8772:2])
  # return bytes(bbuf)

if __name__ == '__main__':
  import sys
  with open(sys.argv[1], 'r') as f:
    bin_content = fm2_to_bin(f)
  with open(sys.argv[2], 'wb') as f:
    f.write(bin_content)

