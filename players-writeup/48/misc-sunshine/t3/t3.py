import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

def getJson():
    return json.loads(open("t3.json", "r").read())
pcap = getJson()

rikeyid = 1485042510
rikey = "F3CB8CFA676D563BBEBFC80D3943F10A"
gcmkey = bytes.fromhex(rikey)

opus_pkts = []

for pkt in pcap:
    data = ""
    try:
        data = pkt['_source']['layers']['data']['data.data']
    except KeyError:
        print(pkt['_source']['layers']['data'])
        continue
    bins = bytes.fromhex(data.replace(':', ''))
    t = bins[1]
    seq = bins[2] << 8 | bins[3]
    payload = bins[12:]
    if t == 127: continue
    assert(t == 97)
    iv = struct.pack('>i', rikeyid+seq) + b'\x00'*12
    cipher = AES.new(gcmkey, AES.MODE_CBC, iv)
    opus = unpad(cipher.decrypt(payload), 16)
    opus_pkts.append(opus)

for i, opus in enumerate(opus_pkts):
    with open(f"t3src-{i}.in", "wb") as f:
        f.write(opus)