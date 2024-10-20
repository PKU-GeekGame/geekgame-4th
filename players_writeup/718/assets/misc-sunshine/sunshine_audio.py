import pyshark
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pickle
import os


rikeyid = 1485042510
rikey = b'\xF3\xCB\x8C\xFA\x67\x6D\x56\x3B\xBE\xBF\xC8\x0D\x39\x43\xF1\x0A'
pcap_file = 'WLAN.pcap'
udp_stream_id = 14
server_ip = '192.168.137.1'


def extract_udp_stream(pcap_file, udp_stream_id, server_ip=None, server_port=None):
    capture = pyshark.FileCapture(pcap_file, display_filter=f'udp.stream eq {udp_stream_id}')
    server_packets = []
    for packet in capture:
        if 'UDP' in packet:
            udp_layer = packet.udp
            if server_ip and packet.ip.src == server_ip:
                server_packets.append(packet)
            elif server_port and udp_layer.srcport == str(server_port):
                server_packets.append(packet)
    capture.close()
    return server_packets


def decrypt_audio_pkt(p):
    typ = p[1]
    seq = int.from_bytes(p[2:4], 'big')
    if typ == 127:
        return  # fec
    assert typ == 97
    b = p[12:]
    iv = struct.pack('>i', rikeyid+seq) + b'\x00'*12
    cipher = AES.new(rikey, AES.MODE_CBC, iv)
    r = cipher.decrypt(b)
    return unpad(r, 16)


if os.path.exists('udp14.pkl'):
    server_packets = pickle.load(open('udp14.pkl', 'rb'))
else:
    server_packets = extract_udp_stream(pcap_file, udp_stream_id, server_ip)
    pickle.dump(server_packets, open('udp14.pkl', 'wb'))

opus = []
for packet in server_packets:
    payload = bytes.fromhex(packet.udp.payload.replace(":", ""))
    decrypt_payload = decrypt_audio_pkt(payload)
    if decrypt_payload:
        opus.append(decrypt_payload)
pickle.dump(opus, open('udp14_opus.pkl', 'wb'))
