import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import opuslib
import opuslib.api
import opuslib.api.decoder
import opuslib.api.ctl
import numpy as np
import soundfile as sf

def decrypt_audio_pkt(p):
    typ = int(p['_source']['layers']['rtp']['rtp.p_type'])
    seq = int(p['_source']['layers']['rtp']['rtp.seq'])
    if typ==127: return # fec
    assert typ==97
    
    b = bytes.fromhex(p['_source']['layers']['rtp']['rtp.payload'].replace(':', ''))
    iv = struct.pack('>i', int('1485042510')+seq) + b'\x00'*12 # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L1516
    cipher = AES.new(bytes.fromhex('F3CB8CFA676D563BBEBFC80D3943F10A'), AES.MODE_CBC, iv)
    
    return unpad(cipher.decrypt(b), 16)

with open('sunshine-audio.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mydecoder = opuslib.api.decoder.create_state(48000, 2)
all_pcm_data = []

for p in data:
    q = decrypt_audio_pkt(p)
    if q == None: continue
    dec = opuslib.api.decoder.decode_float(mydecoder, q, len(q), 480, False)
    frame_size = 480
    channels = 2
    decoded_pcm = struct.unpack('<{}f'.format(frame_size * channels), dec)
    all_pcm_data.extend(decoded_pcm)

all_pcm_data = np.array(all_pcm_data).reshape(-1, 2)

sf.write('sunshine-audio.wav', all_pcm_data, 48000, subtype='FLOAT')

# 2 8 2 5 6 2 8 2 5 7 2 8 2 9 3 1

# flag{2825628257282931}