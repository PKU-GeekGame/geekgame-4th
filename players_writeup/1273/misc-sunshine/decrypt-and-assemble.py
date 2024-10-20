import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

def decrypt_audio_pkt(p):
    typ = int(p['_source']['layers']['rtp']['rtp.p_type'])
    seq = int(p['_source']['layers']['rtp']['rtp.seq'])
    if typ==127: return # fec
    assert typ==97
    
    b = bytes.fromhex(p['_source']['layers']['rtp']['rtp.payload'].replace(':', ''))
    iv = struct.pack('>i', 1485042510+seq) + b'\x00'*12 # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L1516
    cipher = AES.new(bytes.fromhex('F3CB8CFA676D563BBEBFC80D3943F10A'), AES.MODE_CBC, iv)
    
    return unpad(cipher.decrypt(b), 16)

def ogg_page(data, seqn, byte):
    page = bytearray('OggS\x00', 'ascii') + byte
    page += bytes.fromhex('00 00 00 00 00 00 00 00')
    page += bytes.fromhex('de ad be ef')
    page += struct.pack('i',seqn)
    crc_off = len(page)
    page += bytes.fromhex('00 00 00 00')
    page += b'\x01' + struct.pack('b', len(data))
    page += data
    return page[:crc_off] + struct.pack('I', crc_poly(page, 32, 0x04c11db7)) + page[crc_off+4:]

# begin https://gist.github.com/Lauszus/6c787a3bc26fea6e842dfb8296ebd630

def reflect_data(x, width):
    # See: https://stackoverflow.com/a/20918545
    if width == 8:
        x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
        x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
        x = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4)
    elif width == 16:
        x = ((x & 0x5555) << 1) | ((x & 0xAAAA) >> 1)
        x = ((x & 0x3333) << 2) | ((x & 0xCCCC) >> 2)
        x = ((x & 0x0F0F) << 4) | ((x & 0xF0F0) >> 4)
        x = ((x & 0x00FF) << 8) | ((x & 0xFF00) >> 8)
    elif width == 32:
        x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
        x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
        x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
        x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
        x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
    else:
        raise ValueError('Unsupported width')
    return x

def crc_poly(data, n, poly, crc=0, ref_in=False, ref_out=False, xor_out=0):
    g = 1 << n | poly  # Generator polynomial

    # Loop over the data
    for d in data:
        # Reverse the input byte if the flag is true
        if ref_in:
            d = reflect_data(d, 8)

        # XOR the top byte in the CRC with the input byte
        crc ^= d << (n - 8)

        # Loop over all the bits in the byte
        for _ in range(8):
            # Start by shifting the CRC, so we can check for the top bit
            crc <<= 1

            # XOR the CRC if the top bit is 1
            if crc & (1 << n):
                crc ^= g

    # Reverse the output if the flag is true
    if ref_out:
        crc = reflect_data(crc, n)

    # Return the CRC value
    return crc ^ xor_out

# end https://gist.github.com/Lauszus/6c787a3bc26fea6e842dfb8296ebd630

packets = json.loads(open('audio-packets.json', 'r').read())
seq=0
with open('out.opus','wb') as f:
    head = b'OpusHead\x01\x02\x00\x00'
    head += struct.pack('i', 48000) + b'\x00\x00\x00'
    f.write(ogg_page(head, seqn, b'\x02')); seq += 1
    tags = b'OpusTags' + struct.pack('i', 0) + struct.pack('i', 0)
    f.write(ogg_page(tags, seqn, b'\x00')); seq += 1
    for pkt in packets:
        if data := decrypt_audio_pkt(pkt):
            f.write(ogg_page(data, seqn, b'\x00')); seq += 1
    f.write(ogg_page(b'', seqn, b'\x04'))
