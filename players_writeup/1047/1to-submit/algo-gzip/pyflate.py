class BitfieldBase:
    def __init__(self, x):
        if isinstance(x,BitfieldBase):
            self.f = x.f
            self.bits = x.bits
            self.bitfield = x.bitfield
            self.count = x.bitfield
        else:
            self.f = x
            self.bits = 0
            self.bitfield = 0x0
            self.count = 0
    def _read(self, n):
        s = self.f.read(n)
        if not s:
            raise "Length Error"
        self.count += len(s)
        return s
    def needbits(self, n):
        while self.bits < n:
            self._more()
    def _mask(self, n):
        return (1 << n) - 1
    def toskip(self):
        return self.bits & 0x7
    def align(self):
        self.readbits(self.toskip())
    def dropbits(self, n = 8):
        while n >= self.bits and n > 7:
            n -= self.bits
            self.bits = 0
            n -= len(self.f._read(n >> 3)) << 3
        if n:
            self.readbits(n)
        # No return value
    def dropbytes(self, n = 1):
        self.dropbits(n << 3)
    def tell(self):
        # (how many bytes remain, how many bits remain in the current reading byte)
        return self.count - ((self.bits+7) >> 3), 7 - ((self.bits-1) & 0x7)
    def tellbits(self):
        # how many bits remain
        bytes, bits = self.tell()
        return (bytes << 3) + bits

class Bitfield(BitfieldBase):
    def _more(self):
        c = self._read(1)
        self.bitfield += ord(c) << self.bits
        self.bits += 8
    def snoopbits(self, n = 8):
        if n > self.bits:
            self.needbits(n)
        return self.bitfield & self._mask(n)
    def readbits(self, n = 8):
        if n > self.bits:
            self.needbits(n)
        r = self.bitfield & self._mask(n)
        self.bits -= n
        self.bitfield >>= n
        return r

class RBitfield(BitfieldBase):
    def _more(self):
        c = self._read(1)
        self.bitfield <<= 8
        self.bitfield += ord(c)
        self.bits += 8
    def snoopbits(self, n = 8):
        if n > self.bits:
            self.needbits(n)
        return (self.bitfield >> (self.bits - n)) & self._mask(n)
    def readbits(self, n = 8):
        if n > self.bits:
            self.needbits(n)
        r = (self.bitfield >> (self.bits - n)) & self._mask(n)
        self.bits -= n
        self.bitfield &= ~(self._mask(n) << self.bits)
        return r

def printbits(v, n):
    o = ''
    for i in range(n):
        if v & 1:
            o = '1' + o
        else:
            o = '0' + o
        v >>= 1
    return o

class HuffmanLength:
    def __init__(self, code, bits = 0):
        self.code = code
        self.bits = bits
        self.symbol = None
    def __repr__(self):
        return repr((self.code, self.bits, self.symbol, self.reverse_symbol))
    def __lt__(self, other):
        if self.bits == other.bits:
            return self.code < other.code
        else:
            return self.bits < other.bits

def reverse_bits(v, n):
    a = 1 << 0
    b = 1 << (n - 1)
    z = 0
    for i in range(n-1, -1, -2):
        z |= (v >> i) & a
        z |= (v << i) & b
        a <<= 1
        b >>= 1
    return z

def reverse_bytes(v, n):
    a = 0xff << 0
    b = 0xff << (n - 8)
    z = 0
    for i in range(n-8, -8, -16):
        z |= (v >> i) & a
        z |= (v << i) & b
        a <<= 8
        b >>= 8
    return z

symbol_map_table = {}
class HuffmanTable:
    def __init__(self, bootstrap):
        l = []
        start, bits = bootstrap[0]
        for finish, endbits in bootstrap[1:]:
            if bits:
                for code in range(start, finish):
                    l.append(HuffmanLength(code, bits))
            start, bits = finish, endbits
            if endbits == -1:
                break
        l.sort()
        self.table = l

    def populate_huffman_symbols(self):
        bits, symbol = -1, -1
        for x in self.table:
            symbol += 1
            if x.bits != bits:
                symbol <<= (x.bits - bits)
                bits = x.bits
            x.symbol = symbol
            x.reverse_symbol = reverse_bits(symbol, bits)
            #print printbits(x.symbol, bits), printbits(x.reverse_symbol, bits)

    def min_max_bits(self):
        self.min_bits, self.max_bits = 16, -1
        for x in self.table:
            if x.bits < self.min_bits: self.min_bits = x.bits
            if x.bits > self.max_bits: self.max_bits = x.bits

    def _find_symbol(self, bits, symbol, table):
        for h in table:
            if h.bits == bits and h.reverse_symbol == symbol:
                #print "found, processing", h.code
                return h.code
        return -1

    def find_next_symbol(self, field, reversed = True):
        cached_length = -1
        cached = None
        for x in self.table:
            if cached_length != x.bits:
                cached = field.snoopbits(x.bits)
                cached_length = x.bits
            if (reversed and x.reverse_symbol == cached) or (not reversed and x.symbol == cached):
                field.readbits(x.bits)
                print("found symbol", hex(cached), "of len", cached_length, "mapping to", hex(x.code))
                global symbol_map_table
                if x.code != 0x100:
                    symbol_map_table[cached] = chr(x.code)
                return x.code
        raise "unfound symbol, even after end of table @ " + repr(field.tell())

class OrderedHuffmanTable(HuffmanTable):
    def __init__(self, lengths):
        l = len(lengths)
        # z = map(None, list(range(l)), lengths) + [(l, -1)]
        z = []
        for i in range(l):
            z.append((i, lengths[i]))
        z.append((l, -1))
        print("lengths to spans:", z)
        HuffmanTable.__init__(self, z)

def code_length_orders(i):
    return (16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15)[i]

def distance_base(i):
    return (1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577)[i]

def length_base(i):
    return (3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258)[i-257]

def extra_distance_bits(n):
    if 0 <= n <= 1:
        return 0
    elif 2 <= n <= 29:
        return (n >> 1) - 1
    else:
        raise "illegal distance code"

def extra_length_bits(n):
    if 257 <= n <= 260 or n == 285:
        return 0
    elif 261 <= n <= 284:
        return ((n-257) >> 2) - 1
    else:
        raise "illegal length code"

# Sixteen bits of magic have been removed by the time we start decoding
def gzip_main(field):
    b = Bitfield(field)
    method = b.readbits(8)
    if method != 8:
        raise "Unknown (not type eight DEFLATE) compression method"

    # Use flags, drop modification time, extra flags and OS creator type.
    flags = b.readbits(8)
    print('flags', hex(flags))
    mtime = b.readbits(32)
    print('mtime', hex(mtime))
    extra_flags = b.readbits(8)
    print('extra_flags', hex(extra_flags))
    os_type = b.readbits(8)
    print('os_type', hex(os_type))

    if flags & 0x04: # structured GZ_FEXTRA miscellaneous data
        xlen = b.readbits(16)
        b.dropbytes(xlen)
    while flags & 0x08: # original GZ_FNAME filename
        if not b.readbits(8):
            break
    while flags & 0x10: # human readable GZ_FCOMMENT
        if not b.readbits(8):
            break
    if flags & 0x02: # header-only GZ_FHCRC checksum
        b.readbits(16)

    print("gzip header skip", b.tell())
    out = ''

    #print 'header 0 count 0 bits', b.tellbits()

    num_blocks = 0
    while True:
        num_blocks += 1
        header_start = b.tell()
        bheader_start = b.tellbits()
        print('new block at', b.tell())
        lastbit = b.readbits(1)
        print("last bit", hex(lastbit))
        blocktype = b.readbits(2)
        print("deflate-blocktype", blocktype, ["stored", "static huff", "dyna huff"][blocktype], 'beginning at', header_start)

        print('raw block data at', b.tell())
        if blocktype == 0:
            b.align()
            length = b.readbits(16)
            if length & b.readbits(16):
                raise "stored block lengths do not match each other"
            #print "stored block of length", length
            #print 'raw data at', b.tell(), 'bits', b.tellbits() - bheader_start
            #print 'header 0 count 0 bits', b.tellbits() - bheader_start
            for i in range(length):
                out += chr(b.readbits(8))
            #print 'linear', b.tell()[0], 'count', length, 'bits', b.tellbits() - bheader_start

        elif blocktype == 1 or blocktype == 2: # Huffman
            main_literals, main_distances = None, None

            if blocktype == 1: # Static Huffman
                static_huffman_bootstrap = [(0, 8), (144, 9), (256, 7), (280, 8), (288, -1)]
                static_huffman_lengths_bootstrap = [(0, 5), (32, -1)]
                main_literals = HuffmanTable(static_huffman_bootstrap)
                main_distances = HuffmanTable(static_huffman_lengths_bootstrap)

            elif blocktype == 2: # Dynamic Huffman
                dyna_start = b.tellbits()
                len_codes = b.readbits(5)
                literals = len_codes + 257
                distances = b.readbits(5) + 1
                code_lengths_length = b.readbits(4) + 4
                print("Dynamic Huffman tree: length codes: %s, distances codes: %s, code_lengths_length: %s" % \
                    (len_codes, distances, code_lengths_length))

                l = [0] * 19
                for i in range(code_lengths_length):
                    l[code_length_orders(i)] = b.readbits(3)
                print("lengths:", l)

                dynamic_codes = OrderedHuffmanTable(l)
                dynamic_codes.populate_huffman_symbols()
                dynamic_codes.min_max_bits()

                # Decode the code_lengths for both tables at once,
                # then split the list later

                code_lengths = []
                n = 0
                while n < (literals + distances):
                    r = dynamic_codes.find_next_symbol(b)
                    if 0 <= r <= 15: # literal bitlength for this code
                        count = 1
                        what = r
                    elif r == 16: # repeat last code
                        count = 3 + b.readbits(2)
                        # Is this supposed to default to '0' if in the zeroth position?
                        what = code_lengths[-1]
                    elif r == 17: # repeat zero
                        count = 3 + b.readbits(3)
                        what = 0
                    elif r == 18: # repeat zero lots
                        count = 11 + b.readbits(7)
                        what = 0
                    else:
                        raise "next code length is outside of the range 0 <= r <= 18"
                    code_lengths += [what] * count
                    n += count

                print("Literals/len lengths:", code_lengths[:literals])
                print("Dist lengths:", code_lengths[literals:])
                main_literals = OrderedHuffmanTable(code_lengths[:literals])
                main_distances = OrderedHuffmanTable(code_lengths[literals:])
                print("Read dynamic huffman tables", b.tellbits() - dyna_start, "bits")

            # Common path for both Static and Dynamic Huffman decode now

            data_start = b.tell()
            print('raw data at', data_start, 'bits', b.tellbits() - bheader_start)
            #print 'header 0 count 0 bits', b.tellbits() - bheader_start

            main_literals.populate_huffman_symbols()
            main_distances.populate_huffman_symbols()

            main_literals.min_max_bits()
            main_distances.min_max_bits()

            literal_count = 0
            literal_start = b.tellbits()

            while True:
                lz_start = b.tellbits()
                print(lz_start, bin(b.snoopbits(6))[2:].rjust(6, '0'))
                r = main_literals.find_next_symbol(b)
                if 0 <= r <= 255:
                    if literal_count == 0:
                        literal_start = lz_start
                    literal_count += 1
                    print('found literal', repr(chr(r)))
                    out += chr(r)
                elif r == 256:
                    if literal_count > 0:
                        #print 'add 0 count', literal_count, 'bits', lz_start-literal_start, 'data', `out[-literal_count:]`
                        literal_count = 0
                    print('eos 0 count 0 bits', b.tellbits() - lz_start)
                    print('end of Huffman block encountered')
                    break
                elif 257 <= r <= 285: # dictionary lookup
                    assert False
                    if literal_count > 0:
                        #print 'add 0 count', literal_count, 'bits', lz_start-literal_start, 'data', `out[-literal_count:]`
                        literal_count = 0
                    print("reading", extra_length_bits(r), "extra bits for len")
                    length_extra = b.readbits(extra_length_bits(r))
                    length = length_base(r) + length_extra
                    
                    r1 = main_distances.find_next_symbol(b)
                    if 0 <= r1 <= 29:
                        print("reading", extra_distance_bits(r1), "extra bits for dist")
                        distance = distance_base(r1) + b.readbits(extra_distance_bits(r1))
                        cached_length = length
                        while length > distance:
                            out += out[-distance:]
                            length -= distance
                        if length == distance:
                            out += out[-distance:]
                        else:
                            out += out[-distance:length-distance]
                        print('dictionary lookup: length', cached_length, end=' ')
                        print('copy', -distance, 'num bits', b.tellbits() - lz_start, 'data', repr(out[-cached_length:]))
                    elif 30 <= r1 <= 31:
                        raise "illegal unused distance symbol in use @" + repr(b.tell())
                elif 286 <= r <= 287:
                    raise "illegal unused literal/length symbol in use @" + repr(b.tell())
        elif blocktype == 3:
            raise "illegal unused blocktype in use @" + repr(b.tell())

        if lastbit:
            print("this was the last block, time to leave", b.tell())
            break

    footer_start = b.tell()
    bfooter_start = b.tellbits()
    b.align()
    crc = b.readbits(32)
    final_length = b.readbits(32)
    #print len(out)
    next_unused = b.tell()
    #print 'deflate-end-of-stream', 5, 'beginning at', footer_start, 'raw data at', next_unused, 'bits', b.tellbits() - bfooter_start
    print('deflate-end-of-stream')
    print('num of blocks:', num_blocks)
    #print 'crc', hex(crc), 'final length', final_length
    #print 'header 0 count 0 bits', b.tellbits()-bfooter_start

    return out

import sys

def _main():
    filename = sys.argv[1]
    input = open(filename, 'rb')
    field = RBitfield(input)

    magic = field.readbits(16)
    if magic == 0x1f8b: # GZip
        out = gzip_main(field)
    elif magic == 0x425a: # BZip2
        out = bzip2_main(field)
    else:
        raise "Unknown file magic "+hex(magic)+", not a gzip/bzip2 file"

    # f = open('out', 'wb')
    # f.write(out)
    # f.close()
    # input.close()
        
if __name__=='__main__':
    if len(sys.argv) != 2:
        program = sys.argv[0]
        print(program +':', 'usage:', program, '<filename.gz>|<filename.bz2>')
        print('\tThe contents will be decoded and decompressed plaintext written to "./out".')
        sys.exit(0)

    profile_code = False
    if not profile_code:
        try:
            import psyco
            psyco.full()
            profile_code = False
        except:
            pass
    if profile_code:
        import profile
        profile.run('_main()')
    else:
        _main()

    mapping = ""
    for x in range(64):
        if x not in symbol_map_table:
            mapping += '?'
        else:
            mapping += symbol_map_table[x]
    print(mapping)