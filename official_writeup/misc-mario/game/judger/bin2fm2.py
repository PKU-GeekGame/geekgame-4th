#!/usr/bin/env python3


FM2_SMB1_HEADER = '''version 3
emuVersion 20606
rerecordCount 0
palFlag 0
romFilename Super Mario Bros. (W) [!]
romChecksum base64:jjYwGG411HcjG/j9UOVM3Q==
guid 66D34683-2BB6-AAE1-8FFD-3938D0500FB4
fourscore 0
microphone 0
port0 1
port1 1
port2 0
FDS 0
NewPPU 0
RAMInitOption 0
RAMInitSeed 1164944147
|1|........|........||
'''


BUTTONS = ['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']


def int_to_input(i: int) -> str:
  '''
  Converts a byte to a string of 8 buttons.
  '''
  buttons = ''.join(BUTTONS[b] if (i & (1 << b)) else '.'
                    for b in range(7, -1, -1))
  return f'|0|{buttons}|........||\n'


def bin_to_fm2(bin: bytes) -> str:
  '''
  Converts the given binary data of per-frame input to an FM2 file.
  '''
  fm2 = FM2_SMB1_HEADER
  for b in bin:
    fm2 += int_to_input(b)
  return fm2


if __name__ == '__main__':
  import sys
  with open(sys.argv[1], 'rb') as f:
    fm2 = bin_to_fm2(f.read())
  with open(sys.argv[2], 'w') as f:
    f.write(fm2)
