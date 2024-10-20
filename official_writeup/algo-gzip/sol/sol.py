import io
import gzip
import random

import deflate

CONST_XOR = 21
CONST_SEED = 1919

def manip_trivial(text):
    text = [c ^ CONST_XOR for c in text]
    random.seed(CONST_SEED)
    random.shuffle(text)
    text = bytes(text)
    return text
def rev_trivial(s):
    idx = list(range(len(s)))
    random.seed(CONST_SEED)
    random.shuffle(idx)
    
    out = [0]*len(s)
    for i, x in enumerate(idx):
        out[x] = s[i] ^ CONST_XOR
    ret = bytes(out)
    
    assert manip_trivial(ret)==s
    return ret.decode()

alphabet = list(range(0x30, 0x30+64))
alphabet = [x ^ CONST_XOR for x in alphabet]

pad = deflate.make_pad(alphabet, 3)
compressed = gzip.compress(pad)

deflate.TARGET = b'[[What can I say? Mamba out! --KobeBryant]]'
deflate.decode(io.BytesIO(compressed))

assert len(deflate.RESULT_NULL)<1000
assert len(deflate.RESULT_TARGET)<1000
print('\nPayload 1:', rev_trivial(deflate.RESULT_NULL))
print('\nPayload 2:', rev_trivial(deflate.RESULT_TARGET))

print('\n\n----- verify\n')

verify_target = gzip.compress(deflate.RESULT_TARGET)
print(verify_target)
#deflate.decode(io.BytesIO(verify_target))
assert deflate.TARGET in verify_target

verify_null = gzip.compress(deflate.RESULT_NULL)
tot = 0
for c in verify_null[:256]:
    tot += c.bit_count()
assert tot<256*2.5