import pyshark

cap = pyshark.FileCapture(
    'WLAN.pcap',
    display_filter='ip.src == 192.168.137.1 && ip.dst == 192.168.137.68 && udp.srcport == 47998 && !icmp',
    decode_as={'udp.port==47998': 'rtp'}
)

packet_list = sorted(list(cap), key=lambda x: x.rtp.timestamp)

data = b''
current_timestamp = None

for packet in cap:
    print(packet.rtp.seq, packet.rtp.timestamp)
    rtp_payload = bytes.fromhex(str(packet.rtp.payload).replace(":", ""))

    if current_timestamp != packet.rtp.timestamp:
        # assert current_timestamp is None or int(current_timestamp) < int(packet.rtp.timestamp), f"{current_timestamp} | {packet.rtp.timestamp}"
        current_timestamp = packet.rtp.timestamp
        data += rtp_payload[16+4+8:]
    else:
        data += rtp_payload[16+4:]


with open("flag2.h264", "wb") as f:
    f.write(data)
