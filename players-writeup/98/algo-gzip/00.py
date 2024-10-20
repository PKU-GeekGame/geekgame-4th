import gzip
import io
import os
import random

from pyflate import RBitfield, gzip_main


os.chdir(os.path.dirname(__file__))

CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+"

random.seed(114514)
input = [ord(c) ^ 27 for c in CHARACTERS * 4]
random.shuffle(input)

text = gzip.compress(bytes(input))

reader = io.BytesIO(text)
field = RBitfield(reader)

magic = field.readbits(16)
assert magic == 0x1F8B
output = gzip_main(field)

assert bytes(output) == bytes(input)
