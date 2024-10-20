# FROM debian:12
# RUN apt update && apt install -y python3 python3-pip

import random
import gzip

from pathlib import Path
try:
    FLAG1 = Path('/flag1').read_text().strip()
    FLAG2 = Path('/flag2').read_text().strip()
except Exception:
    FLAG1 = 'fake{get flag1 on the real server}'
    FLAG2 = 'fake{get flag2 on the real server}'

def average_bit_count(s):
    return sum(c.bit_count() for c in s) / len(s)

def print_hex(text):
    for i in range(len(text)):
        if i % 16 == 0:
            print('0x' + format(i, '04x'), end='   ')
        print(format(text[i], '02x'), end=' ')
        if i % 16 == 7:
            print('  ', end='')
        if i % 16 == 15:
            print()
    print()

def print_bits(text):
    for i in range(len(text)):
        if i % 8 == 0:
            print('0x' + format(i, '04x'), end='   ')
        print(format(text[i], '08b')[::-1], end=' ')
        if i % 8 == 7:
            print()
    print()

def to_bits(text):
    res = ''
    for i in range(len(text)):
        res += format(text[i], '08b')[::-1]
    res = [(ord(i) - ord('0')) for i in res]
    return res

def get_int(bits, start, len, order=0):
    res = 0
    t = 1
    if order == 1: # 大端
        for i in range(len):
            res += bits[start + len - i - 1] * t
            t *= 2
    else:
        for i in range(len):
            res += bits[start + i] * t
            t *= 2
    return res

def print_b(bits, start, end):
    for i in range(start, end):
        print(bits[i], end='')

class TreeNode:
    def __init__(self, parent, zero, one, ch) -> None:
        self.zero = zero
        self.one = one
        self.ch = ch
        self.set_parent(parent)
    
    def set_ch(self, ch) -> None:
        self.ch = ch
 
    def set_parent(self, parent) -> None:
        self.parent = parent
        if parent != None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
    
    def set_left_child(self, child) -> None:
        self.zero = child
        child.set_parent(self)
    
    def set_right_child(self, child) -> None:
        self.one = child
        child.set_parent(self)
    
    def add_left_child(self) -> None:
        self.set_left_child(TreeNode(None, None, None, 0))
    
    def add_right_child(self) -> None:
        self.set_right_child(TreeNode(None, None, None, 0))
    
    def is_leaf(self) -> bool:
        return self.zero == None and self.one == None

class HuffmanTree:
    def __init__(self) -> None:
        self.root = None
    
    def build_tree(self, length, num=-1) -> None:
        if num == -1:
            num = len(length)
        # leaf_notes = []
        # for i in range(num):
        #     leaf_notes.append(TreeNode(None, None, None, i))
        length_with_id = [(i, length[i]) for i in range(num)]
        length_sorted = sorted(length_with_id, key=lambda x: x[1] * 1000 + x[0])
        current_node = TreeNode(None, None, None, 0)
        self.root = current_node
        for i, l in length_sorted:
            if l == 0:
                continue
            while current_node.depth < l:
                if current_node.zero == None:
                    current_node.add_left_child()
                    current_node = current_node.zero
                elif current_node.one == None:
                    current_node.add_right_child()
                    current_node = current_node.one
                else:
                    current_node = current_node.parent
            current_node.set_ch(i)
            current_node = current_node.parent
    
    def print_tree_node(self, current_node, prefix) -> None:
        if current_node == None:
            return
        if current_node.is_leaf():
            print(prefix + ': ' + str(current_node.ch))
            return
        self.print_tree_node(current_node.zero, prefix + '0')
        self.print_tree_node(current_node.one, prefix + '1')
    
    def print_tree(self) -> None:
        self.print_tree_node(self.root, '')

    def digest(self, bits, start):
        if self.root == None:
            raise 'The tree is empty.'
        current_node = self.root
        pos = start
        while not current_node.is_leaf():
            if bits[pos] == 0:
                current_node = current_node.zero
            else:
                current_node = current_node.one
            pos += 1
        return pos, current_node.ch

def digest_length(bits, start, ch):
    if ch <= 256:
        raise 'ch error.'
    if ch <= 264:
        return start, ch - 254
    elif ch <= 268:
        return start + 1, 11 + (ch - 265) * 2 + get_int(bits, start, 1, 1)
    elif ch <= 272:
        return start + 2, 19 + (ch - 269) * 4 + get_int(bits, start, 2, 1)
    elif ch <= 276:
        return start + 3, 35 + (ch - 273) * 8 + get_int(bits, start, 3, 1)
    elif ch <= 280:
        return start + 4, 67 + (ch - 277) * 16 + get_int(bits, start, 4, 1)
    elif ch <= 284:
        return start + 5, 131 + (ch - 281) * 32 + get_int(bits, start, 5, 1)
    else:
        return start, 258

def digest_distance(bits, start, dist_tree):
    # code = get_int(bits, start, 5, 1)
    # start += 5
    start, code = dist_tree.digest(bits, start)
    if code <= 3:
        return start, code + 1
    elif code <= 5:
        return start + 1, 5 + (code - 4) * 2 + get_int(bits, start, 1, 1)
    elif code <= 7:
        return start + 2, 9 + (code - 6) * 4 + get_int(bits, start, 2, 1)
    elif code <= 9:
        return start + 3, 17 + (code - 8) * 8 + get_int(bits, start, 3, 1)
    elif code <= 11:
        return start + 4, 33 + (code - 10) * 16 + get_int(bits, start, 4, 1)
    elif code <= 13:
        return start + 5, 65 + (code - 12) * 32 + get_int(bits, start, 5, 1)
    elif code <= 15:
        return start + 6, 129 + (code - 14) * 64 + get_int(bits, start, 6, 1)
    elif code <= 17:
        return start + 7, 257 + (code - 16) * 128 + get_int(bits, start, 7, 1)
    elif code <= 19:
        return start + 8, 513 + (code - 18) * 256 + get_int(bits, start, 8, 1)
    elif code <= 21:
        return start + 9, 1025 + (code - 20) * 512 + get_int(bits, start, 9, 1)
    elif code <= 23:
        return start + 10, 2049 + (code - 22) * 1024 + get_int(bits, start, 10, 1)
    elif code <= 25:
        return start + 11, 4097 + (code - 24) * 2048 + get_int(bits, start, 11, 1)
    elif code <= 27:
        return start + 12, 8193 + (code - 26) * 4096 + get_int(bits, start, 12, 1)
    elif code <= 29:
        return start + 13, 16385 + (code - 28) * 8192 + get_int(bits, start, 13, 1)
    else:
        raise 'distance code error.'

def digest_int(bits, start, len, ord):
    i = get_int(bits, start, len, ord)
    return start + len, i

def explain_block(bits):
    print('BFINAL =', bits[0], '   -- this is ' + ('' if bits[0] == 1 else 'not ') + 'the final block')
    compression_type_str = ['no compression', 'compressed with fixed Huffman codes', 'compressed with dynamic Huffman codes', 'reserved (error)']
    compression_type = get_int(bits, 1, 2)
    print('BTYPE  =', str(bits[2]) + str(bits[1]), '  --', compression_type_str[compression_type])
    lit_tree = HuffmanTree()
    dist_tree = HuffmanTree()
    if compression_type == 0:
        return
    pos = 3
    if compression_type == 1:
        lit_tree.build_tree([8] * 144 + [9] * 112 + [7] * 24 + [8] * 8)
        dist_tree.build_tree([5] * 32)
    elif compression_type == 2:
        HLIT = get_int(bits, pos, 5, 0)
        print_b(bits, pos, pos + 5)
        print('   -- HLIT,', HLIT + 257)
        pos += 5
        HDIST = get_int(bits, pos, 5, 0)
        print_b(bits, pos, pos + 5)
        print('   -- HDIST,', HDIST + 1)
        pos += 5
        HCLEN = get_int(bits, pos, 4, 0)
        print_b(bits, pos, pos + 4)
        print('   -- HCLEN,', HCLEN + 4)
        pos += 4
        code_len_alphabet_len = [0] * 19
        code_len_map = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
        old_pos = pos
        for i in range(HCLEN + 4):
            l = get_int(bits, pos, 3, 0)
            code_len_alphabet_len[code_len_map[i]] = l      # 必须在这里进行映射，如果在后面映射，建的树不符合字典序
            # code_len_alphabet_len[i] = l 
            pos += 3
        print_b(bits, old_pos, pos)
        print('   -- code lengths for code length alphabet')
        print(code_len_alphabet_len)
        code_len_alphabet_tree = HuffmanTree()
        code_len_alphabet_tree.build_tree(code_len_alphabet_len)
        code_len_alphabet_tree.print_tree()

        lit_len = []
        old_pos = pos
        while len(lit_len) < HLIT + 257:
            pos, ch = code_len_alphabet_tree.digest(bits, pos)
            # ch = code_len_map[ch]
            if ch <= 15:
                lit_len.append(ch)
            elif ch == 16:
                pos, i = digest_int(bits, pos, 2, 0)
                lit_len += [lit_len[-1]] * (i + 3)
            elif ch == 17:
                pos, i = digest_int(bits, pos, 3, 0)
                lit_len += [0] * (i + 3)
            elif ch == 18:
                pos, i = digest_int(bits, pos, 7, 0)
                lit_len += [0] * (i + 11)
        print_b(bits, old_pos, pos)
        print('   -- this is the huffman tree for lit/len')
        print(lit_len, len(lit_len), HLIT + 257)
        lit_tree.build_tree(lit_len)
        lit_tree.print_tree()

        dist_len = []
        old_pos = pos
        while len(dist_len) < HDIST + 1:
            pos, ch = code_len_alphabet_tree.digest(bits, pos)
            # ch = code_len_map[ch]
            if ch <= 15:
                dist_len.append(ch)
            elif ch == 16:
                pos, i = digest_int(bits, pos, 2, 0)
                dist_len += [dist_len[-1]] * (i + 3)
            elif ch == 17:
                pos, i = digest_int(bits, pos, 3, 0)
                dist_len += [0] * (i + 3)
            elif ch == 18:
                pos, i = digest_int(bits, pos, 7, 0)
                dist_len += [0] * (i + 11)
        print_b(bits, old_pos, pos)
        print('   -- this is the huffman tree for dist')
        print(dist_len, len(dist_len), HDIST + 1)
        dist_tree.build_tree(dist_len)
        dist_tree.print_tree()
    
    print('current pos:', pos)

    while True:
        new_pos, ch = lit_tree.digest(bits, pos)
        print_b(bits, pos, new_pos)
        print(':', ch, end='')
        pos = new_pos
        if ch < 256:
            print('   -- this is an explicit char:', chr(ch))
        elif ch == 256:
            print('   -- this is end of block')
            break
        else:
            print('   -- this is a length')
            new_pos, l = digest_length(bits, pos, ch)
            print('    ', end='')
            print_b(bits, pos, new_pos)
            print(' -- the length is', l)
            pos = new_pos
            new_pos, d = digest_distance(bits, pos, dist_tree)
            print_b(bits, pos, new_pos)
            print(' -- the distance is', d)
            pos = new_pos

    # default_tree.print_tree()


def main():
    text = input('Input text: ')
    # assert len(text)<=1000
    assert all(0x20<=ord(c)<=0x7e for c in text)
        
    text = [ord(c) ^ 13 for c in text]
    random.seed(1919)
    random.shuffle(text)
    # text = [ord(c) for c in text]

    # for c in text:
    #     print(chr(c ^ 13), end='')
    print('\nBefore gzip:\n')
    print_hex(bytes(text))
    
    text = gzip.compress(bytes(text))
    print('\nAfter processing:\n')
    # print(text)
    print_hex(text)
    print()

    print('header:')
    print_hex(text[:10])
    print()

    print('blocks:')
    print_hex(text[10:-8])
    print()

    print_bits(text[10:-8])
    print()

    bits = to_bits(text[10:-8])
    explain_block(bits)
    print()

    print('footer:')
    print_hex(text[-8:])


    cnt_block = average_bit_count(text[10:-8])
    print('average bit in block:', cnt_block)

    
    prefix = (text + b'\xFF'*256)[:256]
    cnt = average_bit_count(prefix)
    # cnt = average_bit_count(text)

    print('average bit:', cnt)

    print(text)

    if cnt < 2.5:
        print('\nGood! Flag 1: ', FLAG1)
    
    if b'[What can I say? Mamba out! --KobeBryant]' in text:
        print('\nGood! Flag 2: ', FLAG2)
        
try:
    main()
except Exception as e:
    print('Error:', type(e))