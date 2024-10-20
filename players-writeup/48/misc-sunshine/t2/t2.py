import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

def getJson():
    return json.loads(open("t2.json", "r").read())
pcap = getJson()


# for i in range(10):
#     x = pcap[i]["_source"]["layers"]["rtp"]["rtp.payload"].replace(":", "")
#     x = bytes.fromhex(x)
#     nv = struct.unpack("<II4BI", x[:16])
#     print(nv)
#     print()

# exit(0)

fp = open("t2.264", "wb")

ids = []

datastream = b""

for i, pkt in enumerate(pcap):
    try:
        # data = pkt["_source"]["layers"]["udp"]["udp.payload"]
        data = pkt["_source"]["layers"]["rtp"]["rtp.payload"]
    except KeyError:
        continue
    data = data.replace(":", "")
    data = bytes.fromhex(data)
    nv = struct.unpack("<II4BI", data[:16])
    frameId = nv[1]
    fecInfo = nv[6]
    data_shards = fecInfo >> 22
    x = (fecInfo >> 12) & 0x3FF
    precentage = (fecInfo >> 4) & 0xFF
    print(frameId, data_shards, x, precentage)
    if x < data_shards:
        datastream += data[16:][8:]
        # ids.append(nv[1])


fp.write(datastream)
fp.close()
    