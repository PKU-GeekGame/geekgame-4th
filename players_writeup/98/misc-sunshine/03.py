import os
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

RIKEY = bytes.fromhex("F3CB8CFA676D563BBEBFC80D3943F10A")
RIKEYID = 1485042510


os.chdir(os.path.dirname(__file__))
with open("03-filtered.pcap", "rb") as reader:
  pcap_bytes = reader.read()

writer = open("03-decrypted.pcap", "wb")

header = pcap_bytes[:24]
writer.write(header)
pos = 24
while pos < len(pcap_bytes):
  time, time_ns, length, orig_length = struct.unpack("<IIII", pcap_bytes[pos : pos + 16])
  raw_bytes = pcap_bytes[pos + 16 : pos + 16 + length]

  _, typ, seq = struct.unpack(">BBH", raw_bytes[0x2A:0x2E])

  if not typ == 97:
    continue

  encrypted = raw_bytes[0x36:]
  iv = (
    struct.pack(">i", RIKEYID + seq) + b"\x00" * 12
  )  # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L1516
  cipher = AES.new(RIKEY, AES.MODE_CBC, iv)

  # decrypted = cipher.decrypt(encrypted)
  decrypted = unpad(cipher.decrypt(encrypted), 16)
  writer.write(struct.pack("<IIII", time, time_ns, len(decrypted) + 0x36, len(decrypted) + 0x36))
  writer.write(pcap_bytes[pos + 16 : pos + 16 + 0x36] + decrypted)
  pos = pos + 16 + length
