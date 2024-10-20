import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_audio_pkt(p):
    typ = int(p['_source']['layers']['rtp']['rtp.p_type'])
    seq = int(p['_source']['layers']['rtp']['rtp.seq'])
    if typ==127: return # fec
    assert typ==97
    
    b = bytes.fromhex(p['_source']['layers']['rtp']['rtp.payload'].replace(':', ''))
    iv = struct.pack('>i', int('?????????')+seq) + b'\x00'*12 # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L1516
    cipher = AES.new(b'????????????????', AES.MODE_CBC, iv)
    
    return unpad(cipher.decrypt(b), 16)