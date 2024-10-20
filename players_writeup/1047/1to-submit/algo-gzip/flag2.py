# FROM debian:12
# RUN apt update && apt install -y python3 python3-pip

import random
import gzip
import string
import sys

# mapping = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-"
# mapping = "+VEl7dMt3ZIpAhQx1XGn9fOv5bKrCjSz0WFm8eNu4aJqBiRy2YHo=gPw6cLsDkUT"

mapping = "abcdefg.ijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-"
mapping = "+UEl6cMt2YIpAgQx0WGn8eOv4aKrCjSz.VFm7dNu3ZJqBiRy1XHo9fPw5bLsDkT?"

def target2token_id(target: bytes, path_length: int) -> list[int]:
    # Get bit-level representation of `target`, MSB first in each byte
    bits = [b>>i&1 for b in target for i in range(0, 8)]
    bits = [0]*7 + [0, 1, 0, 1, 0, 1, 0, 0] + bits
    # Make it a multiple of `token_length`
    while len(bits) % path_length:
        bits.append(0)
    # Decipher tokens in "target"
    target_tokens = []
    while len(bits):
        cur_bits = bits[:path_length]
        bits = bits[path_length:]
        cur_token = 0
        for index, bit in enumerate(cur_bits):
            cur_token = cur_token | bit << index
        target_tokens.append(cur_token)
    return target_tokens

def equalize_token_counts(crit_tokens: list[int], path_length: int, token_length: int, length_limit: int, token2ignore) -> list[int]:
    token_num_limit = length_limit//token_length
    each_token_num_limit = token_num_limit // (1 << path_length)

    token_app_count = [0] * (1 << path_length)
    for token in crit_tokens:
        assert token != token2ignore
        token_app_count[token] += 1
    max_app_count = max(token_app_count)
    if max_app_count > each_token_num_limit:
        print(f'Critical tokens are too frequent: {max_app_count} > {each_token_num_limit}')
        assert False
    print(f'Critical tokens ({len(crit_tokens)}) takes up {len(crit_tokens)/token_num_limit*100:.2f}% of the space ({token_num_limit})')

    order_def_tokens = []
    # for token_id in range(1<<path_length):
    #     if token_id == token2ignore:
    #         continue
    #     order_def_tokens.append(token_id)
    #     token_app_count[token_id] += 1

    non_crit_tokens = []
    for token_id in range(1<<path_length):
        if token_id == token2ignore:
            continue
        non_crit_tokens += [token_id] * (each_token_num_limit - token_app_count[token_id])
    random.shuffle(non_crit_tokens)

    ans = order_def_tokens + crit_tokens + non_crit_tokens

    # Checkings
    for token in range(1<<path_length):
        if token == token2ignore:
            continue
        assert ans.count(token) == each_token_num_limit

    assert token2ignore not in ans

    return ans

def substitute_tokens(tokens: list[int], path_length: int, token_length: int, unused_token: int) -> list[str]:
    result = []
    for token in tokens:
        assert token != unused_token
        result.append(mapping[token])
    return result

def contains_bit_seq(source: bytes, template: bytes) -> bool:
    def dump_as_bit_seq(data: bytes) -> str:
        # MSB First
        res = ''
        for b in data:
            for i in range(0, 8, 1):
                res += str(b>>i&1)
        return res
    src_res = dump_as_bit_seq(source)
    template_res = dump_as_bit_seq(template)
    print(src_res)
    print(template_res)
    pos = src_res.find(template_res)
    if pos:
        print(pos)
        # assert False
    return pos != -1

random.seed(3)
TOKEN_LENGTH = 1
PATH_LENGTH = 6
TARGET_TEXT = b'[What can I say? Mamba out! --KobeBryant]'

crit_tokens = target2token_id(TARGET_TEXT, PATH_LENGTH)
print("crit tokens:", crit_tokens)

nonused_tokens = list(set(range(1<<PATH_LENGTH)) - set(crit_tokens))
nonused_token = nonused_tokens[-1]
print("unused token:", nonused_token)

tokens = equalize_token_counts(crit_tokens, PATH_LENGTH, TOKEN_LENGTH, 290, nonused_token)
# print(tokens)
results = substitute_tokens(tokens, PATH_LENGTH, TOKEN_LENGTH, nonused_token)
payload = ''.join(results)
print(payload)

for index, ch in enumerate(payload):
    inp = ord(ch) ^ 23
    assert 0x20 <= inp <= 0x7e

compressed = gzip.compress(payload.encode())

is_contained = contains_bit_seq(compressed, TARGET_TEXT)
is_contained2 = TARGET_TEXT in compressed
print(is_contained, is_contained2)
if is_contained2:
    print("GOOD!")
    s = ''.join([chr(ord(c)^23) for c in payload])

    l = len(s)
    reflect = {}
    for pos in range(l):
        tmp_s = [0]*pos + [1] + [0]*(l-pos-1)
        assert len(tmp_s) == l and tmp_s[pos] == 1
        random.seed(8888)
        random.shuffle(tmp_s)
        new_pos = tmp_s.index(1)
        assert new_pos not in reflect
        reflect[new_pos] = pos
    
    ans = ['?']*l
    for new_pos in range(l):
        old_pos = reflect[new_pos]
        ans[old_pos] = s[new_pos]
    print(''.join(ans))

    # sys.exit(1)

def average_bit_count(s):
    return sum(c.bit_count() for c in s) / len(s)

prefix = (compressed + b'\xFF'*256)[:256]
c = average_bit_count(prefix)

print(c)
assert c > 2.5

with open('compressed.gzip', 'wb') as f:
    f.write(compressed)

sys.exit(0)

from pathlib import Path
try:
    FLAG1 = Path('/flag1').read_text().strip()
    FLAG2 = Path('/flag2').read_text().strip()
except Exception:
    FLAG1 = 'fake{get flag1 on the real server}'
    FLAG2 = 'fake{get flag2 on the real server}'

def main():
    # text = input('Input text: ')
    # random.seed(0)
    # text = [random.choice(string.digits + string.ascii_letters) for _ in range(1000)]
    # assert len(text)<=1000
    # assert all(0x20<=ord(c)<=0x7e for c in text)
        
    text = "0" * 256
    for i in range(100):
        place = random.randint(0, len(text))
        text = text[:place] + "1" + text[place:]
    text = [ord(c) ^ 23 for c in text]	# 0x17
    # random.seed(8888)
    # random.shuffle(text)
    
    text = gzip.compress(bytes(text))
    print('\nAfter processing:\n')
    print(text)
    
    print("Average bit count without padding", average_bit_count(text))

    prefix = (text + b'\xFF'*256)[:256]
    c = average_bit_count(prefix)
    print("Average bit count of the first 256 bytes:", c)
    if c < 2.5:
        print('\nGood! Flag 1: ', FLAG1)
    
    if b'[What can I say? Mamba out! --KobeBryant]' in text:
        print('\nGood! Flag 2: ', FLAG2)
        
main()