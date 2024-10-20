import binascii
import struct
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# in debug log for nvhttp /launch
LAUNCH_RIKEYID = 1485042510
LAUNCH_RIKEY = 'F3CB8CFA676D563BBEBFC80D3943F10A'

aes_key = binascii.unhexlify(LAUNCH_RIKEY)

last_seq = -1
def load_pkt(p):
    global last_seq
    typ = int(p['_source']['layers']['rtp']['rtp.p_type'])
    seq = int(p['_source']['layers']['rtp']['rtp.seq'])
    if typ==127: # fec
        return None
    assert typ==97
    
    assert seq==last_seq+1
    last_seq = seq
    
    hextxt = p['_source']['layers']['rtp']['rtp.payload'].replace(':', '')
    b = binascii.unhexlify(hextxt)
    assert len(b)%16==0
    
    # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L1516
    iv = struct.pack('>i', LAUNCH_RIKEYID+seq) + b'\x00'*12
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    plain = unpad(cipher.decrypt(b), 16)
    print(len(plain), plain[:16])
    return plain

with open('data/decoded.opus_raw', 'wb') as fw:
    # udp.srcport == 48000 and rtp
    with open('data/rtp-48000.json', encoding='utf-8') as f:
        for p in json.load(f):
            pp = load_pkt(p)
            if pp:
                fw.write(pp)