import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pyshark
import os

os.makedirs("audioout", exist_ok=True)

cap = pyshark.FileCapture(
    './WLAN.pcap',
    display_filter='ip.src == 192.168.137.1 && ip.dst == 192.168.137.68 && udp.srcport == 48000 && !icmp',
    decode_as={'udp.port==48000': 'rtp'})


def decrypt_audio_pkt(p):
    typ = int(p.rtp.p_type)
    seq = int(p.rtp.seq)
    if typ == 127:
        return b''  # fec
    assert typ == 97

    b = bytes.fromhex(str(p.rtp.payload).replace(':', ''))
    # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L1516
    iv = struct.pack('>i', int('1485042510')+seq) + b'\x00'*12
    cipher = AES.new(bytes.fromhex("F3CB8CFA676D563BBEBFC80D3943F10A"), AES.MODE_CBC, iv)
    t = cipher.decrypt(b)
    return unpad(t, 16)


data = b''
for packet in cap:
    result = decrypt_audio_pkt(packet)
    with open(f"./audioout/{packet.rtp.seq}.dat", 'wb') as f:
        f.write(result)
    print(result.hex())
    data += result

with open('out.dat', 'wb') as f:
    f.write(data)
